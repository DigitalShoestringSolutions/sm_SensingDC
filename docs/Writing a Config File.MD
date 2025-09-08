# Writing a sensing SM config file
## The Config File
The config file has two parts `user config` and `module config`. The `module config` defines a recipe for all of the building blocks that are run by the sensing service module. The `user config` is intended to be modified by an end user to change key values (for example, which adc channel a sensor is attached to). 

The service module checks for the `user config` file in the following locations in order of precedence:
|Location| Details|
|---|---|
| Environment variable |`USER_CONFIG_FILE`|
| Command line arg |`--user_config <filename>`|
| Default location |`/app/user_config/user_config.toml`|

> In most Shoestring scenarios, a Docker volume is used to put the `user config` file in the default location.

The service module checks for the `module config` file in the following locations in order of precedence:

|Location| Details|
|---|---|
| Environment variable |`MODULE_CONFIG_FILE`|
| Command line arg |`--module_config <filename>`|
| Specified in the `user config` file | `module_config_file = "<filename>"` |
| Default location |`/app/module_config/module_config.toml`|

> The `user config` file is the most commonly used option within Shoestring

## How the service module works
The primary element of the sensing service module is the `measurement`. The service module can only use a single `measurement`. The measurements `loop` function is called repeatedly and returns a *delay value* and a *variable set*. If the *variable set* exists (not `None`), the variables are used to generate `output messages` that are sent over MQTT. If the *delay value* is valid, the service module sleeps for the contained duration.

The `measurement` will have one or more `sensing stacks` (depending on the measurement module). A `sensing stack` is the combination of a `device` and a calculation `pipeline` - in essence it describes how a sample is taken from a single attached `device` and the `pipeline` of calculations that are applied to get the required outputs. Implementations that need to sample multiple `devices` will need to specify multiple `sensing stacks` and use a `measurement` that supports multiple. (Different `sensing stacks` can reuse the same calculation `pipeline` with a different device.)

The `sensing stack` and calculation `pipeline` use a *blackboard* approach. In the *blackboard* approach there is a *blackboard* with variable names and values. Each step in the process can add variables and/or change the values of existing variables. In terms of how this is implemented - Sampling the `device` sets the initial values for the *blackboard* (as a `dict`). Each `calculation` in the `pipeline` is then executed, receiving the current *blackboard* as an input and returning the updated *blackboard* as its output. 

> Each `calculation` and `device` in the config file has a `[calculation.<name>.variables]`/`[device.<name>.variables]` section where the *blackboard* variable names are mapped for each `device` and `calculation`. In the example below - the device output is stored on the *blackboard* as `"v_amp_out"` and then the **amplifier** `calculation` is set to use this variable as its **amp_output** value when calculating the **amp_input** value which is stored on the *blackboard* as `"v_amp_in"`. Similarly this variable is then later used by the **current_clamp** `calculation` and the output stored as `"clamp_current"` which in turn is used by the **rms_current** `calculation` to get `"current_rms"` which is used in the `output message`.



## File Format
The config file has 7 main sections:
|Section|Tag|Purpose|
|---|---|---|
|Interface|`[interface.<name>]`||
|Device|`[device.<name>]`||
|Calculations|`[calculation.<name>]`|Defines a set of named calculation modules and their input and output variables|
|Calculation Pipelines|`[pipelines]`|Defines one or more calculation pipelines. A pipeline is a list of calculation modules in the order that they are called.|
|Measurement Specifications|`[measurement]`|Defines and configures the measurement module as specifies the sensing stacks it uses.|
|Output Messages Specification|`[output.<name>]`|Defines how output messages are formed from the variable set returned by the measurement.|
|MQTT Config|`[mqtt]`| Used to specify MQTT broker and port, as well as configure reconnection behaviour |

##### Below is an example from the Power Monitoring Solution that demonstrates these sections:
```
#=-= Define Interface Modules =-=
[interface.spi0]
    module="spi"    # module name in core.interface_modules
    class="SPI"
[interface.spi0.config]
    bus=0
    device=0
    speed=1000000
    mode=0

#=-= Define Device Modules =-=
[device.adc_0]
    module="adc_MCP300X"    # module name in core.device_modules
    class="MCP3008"
    interface="spi0"
[device.adc_0.config]
    adc_channel=0
[device.adc_0.variables]
    v_in = "v_amp_out"

#=-= Define Calculation Modules =-=
[calculation.machine_name]
    module="gen_constants"    # module name in core.calculation_modules
    class="ConstantSet"
[calculation.machine_name.config]
    machine = "Machine_1"
[calculation.machine_name.variables]

[calculation.rms_current]
    module="gen_electrical"
    class="RMSToPeak"
[calculation.rms_current.variables]
    var_in = "current_rms"
    var_out = "clamp_current"

[calculation.current_clamp]
    module="gen_current_clamp"
    class="VoltageClamp"
[calculation.current_clamp.config]
    nominal_current = 20
[calculation.current_clamp.variables]
    current_in = "clamp_current"
    voltage_out = "v_amp_in"

[calculation.amplifier]
    module="gen_amplifier"
    class="GenAmplifier"
[calculation.amplifier.config]
    gain = 2
[calculation.amplifier.variables]
    amp_input = "v_amp_in"
    amp_output = "v_amp_out"

#=-= Define Calculation Pipelines =-=
[pipelines]
    rms_current = ["machine_name","amplifier","current_clamp","rms_current"]

#=-= Define Measurements Pipelines =-=
[measurement]
    module="gen_sample"     # module name in core.measurement_modules
    class="SingleSampleAvg"
[measurement.config]
    period = 1.0 # seconds
    n_samples = 5
[[measurement.sensing_stacks]]
    device = "adc_0"
    pipeline = "single_clamp"
    constants = {'phase'='single'}      # contants added to the blackboard for this sensing stack

[output.overall]
    topic = "power_monitoring/{{machine}}/{{phase}}"    # mustache style template - elements in {{ }} will be replaced from final message contents
[output.overall.message_spec]
    timestamp = '$.timestamp'   # JSONPath lookup from blackboard - can also be fixed values - look at core.output.py for details
    current = "$.current_rms"
    phase = "$.phase"
    machine="$.machine"


[mqtt]
    broker = "mqtt.docker.local"
    port = 1883   #common mqtt ports are 1883 and 8883
    topic_prefix = ""

    #reconnection characteristics
    # start: timeout = initial,
    # if timeout < limit then
    #   timeout = timeout*backoff
    # else
    #   timeout = limit
    reconnect.initial = 5 # seconds
    reconnect.backoff = 2 # multiplier
    reconnect.limit = 60 # seconds
```

## Process to follow when writing / adapting a config file

1. Specify all the `devices` you need
1. Specify the `interfaces` you need for those `devices` and set the `device.<name>.interface` for each
1. Create the `pipelines` that you need to process samples into output values
1. Specify the `calculation` modules needed by the `pipelines`
1. Select the `measurement` and arrange the `pipelines` and `devices` into `sensing stacks`
1. Write the `output message` specs
