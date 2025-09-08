# Data Collection Service Module Config Schema

- [1. Property `Data Collection Service Module Config Schema > interface`](#interface)
  - [1.1. Pattern Property `Data Collection Service Module Config Schema > interface > ^.*$`](#interface_pattern1)
    - [1.1.1. Property `Data Collection Service Module Config Schema > interface > ^.*$ > module`](#interface_pattern1_module)
    - [1.1.2. Property `Data Collection Service Module Config Schema > interface > ^.*$ > class`](#interface_pattern1_class)
    - [1.1.3. Property `Data Collection Service Module Config Schema > interface > ^.*$ > config`](#interface_pattern1_config)
- [2. Property `Data Collection Service Module Config Schema > device`](#device)
  - [2.1. Pattern Property `Data Collection Service Module Config Schema > device > ^.*$`](#device_pattern1)
    - [2.1.1. Property `Data Collection Service Module Config Schema > device > ^.*$ > module`](#device_pattern1_module)
    - [2.1.2. Property `Data Collection Service Module Config Schema > device > ^.*$ > class`](#device_pattern1_class)
    - [2.1.3. Property `Data Collection Service Module Config Schema > device > ^.*$ > interface`](#device_pattern1_interface)
    - [2.1.4. Property `Data Collection Service Module Config Schema > device > ^.*$ > config`](#device_pattern1_config)
    - [2.1.5. Property `Data Collection Service Module Config Schema > device > ^.*$ > variables`](#device_pattern1_variables)
- [3. Property `Data Collection Service Module Config Schema > calculation`](#calculation)
  - [3.1. Pattern Property `Data Collection Service Module Config Schema > calculation > ^.*$`](#calculation_pattern1)
    - [3.1.1. Property `Data Collection Service Module Config Schema > calculation > ^.*$ > module`](#calculation_pattern1_module)
    - [3.1.2. Property `Data Collection Service Module Config Schema > calculation > ^.*$ > class`](#calculation_pattern1_class)
    - [3.1.3. Property `Data Collection Service Module Config Schema > calculation > ^.*$ > config`](#calculation_pattern1_config)
    - [3.1.4. Property `Data Collection Service Module Config Schema > calculation > ^.*$ > variables`](#calculation_pattern1_variables)
- [4. Property `Data Collection Service Module Config Schema > pipelines`](#pipelines)
  - [4.1. Pattern Property `Data Collection Service Module Config Schema > pipelines > ^.*$`](#pipelines_pattern1)
    - [4.1.1. Data Collection Service Module Config Schema > pipelines > ^.*$ > ^.*$ items](#pipelines_pattern1_items)
- [5. Property `Data Collection Service Module Config Schema > measurement`](#measurement)
  - [5.1. Property `Data Collection Service Module Config Schema > measurement > module`](#measurement_module)
  - [5.2. Property `Data Collection Service Module Config Schema > measurement > class`](#measurement_class)
  - [5.3. Property `Data Collection Service Module Config Schema > measurement > config`](#measurement_config)
  - [5.4. Property `Data Collection Service Module Config Schema > measurement > sensing_stacks`](#measurement_sensing_stacks)
    - [5.4.1. Data Collection Service Module Config Schema > measurement > sensing_stacks > sensing_stacks items](#measurement_sensing_stacks_items)
      - [5.4.1.1. Property `Data Collection Service Module Config Schema > measurement > sensing_stacks > sensing_stacks items > device`](#measurement_sensing_stacks_items_device)
      - [5.4.1.2. Property `Data Collection Service Module Config Schema > measurement > sensing_stacks > sensing_stacks items > pipeline`](#measurement_sensing_stacks_items_pipeline)
      - [5.4.1.3. Property `Data Collection Service Module Config Schema > measurement > sensing_stacks > sensing_stacks items > constants`](#measurement_sensing_stacks_items_constants)
      - [5.4.1.4. Property `Data Collection Service Module Config Schema > measurement > sensing_stacks > sensing_stacks items > prefix`](#measurement_sensing_stacks_items_prefix)
- [6. Property `Data Collection Service Module Config Schema > output`](#output)
  - [6.1. Pattern Property `Data Collection Service Module Config Schema > output > ^.*$`](#output_pattern1)
    - [6.1.1. Property `Data Collection Service Module Config Schema > output > ^.*$ > topic`](#output_pattern1_topic)
    - [6.1.2. Property `Data Collection Service Module Config Schema > output > ^.*$ > message_spec`](#output_pattern1_message_spec)
- [7. Property `Data Collection Service Module Config Schema > mqtt`](#mqtt)
  - [7.1. Property `Data Collection Service Module Config Schema > mqtt > broker`](#mqtt_broker)
  - [7.2. Property `Data Collection Service Module Config Schema > mqtt > port`](#mqtt_port)
  - [7.3. Property `Data Collection Service Module Config Schema > mqtt > topic_prefix`](#mqtt_topic_prefix)
  - [7.4. Property `Data Collection Service Module Config Schema > mqtt > reconnect`](#mqtt_reconnect)
    - [7.4.1. Property `Data Collection Service Module Config Schema > mqtt > reconnect > initial`](#mqtt_reconnect_initial)
    - [7.4.2. Property `Data Collection Service Module Config Schema > mqtt > reconnect > backoff`](#mqtt_reconnect_backoff)
    - [7.4.3. Property `Data Collection Service Module Config Schema > mqtt > reconnect > limit`](#mqtt_reconnect_limit)

**Title:** Data Collection Service Module Config Schema

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** A representation of the expected format for the config file for this service module

| Property                       | Pattern | Type   | Deprecated | Definition | Title/Description                                                              |
| ------------------------------ | ------- | ------ | ---------- | ---------- | ------------------------------------------------------------------------------ |
| - [interface](#interface )     | No      | object | No         | -          | Set of interfaces                                                              |
| - [device](#device )           | No      | object | No         | -          | Set of devices                                                                 |
| - [calculation](#calculation ) | No      | object | No         | -          | Set of calculations                                                            |
| - [pipelines](#pipelines )     | No      | object | No         | -          | Specifies one or more calculation pipelines that can be used in sensing stacks |
| - [measurement](#measurement ) | No      | object | No         | -          | Specifies the measurement policy for the service module                        |
| - [output](#output )           | No      | object | No         | -          | Specifies the outputs from this service module                                 |
| - [mqtt](#mqtt )               | No      | object | No         | -          | Contains the configuration for the MQTT client                                 |

## <a name="interface"></a>1. Property `Data Collection Service Module Config Schema > interface`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Set of interfaces

| Property                       | Pattern | Type   | Deprecated | Definition | Title/Description     |
| ------------------------------ | ------- | ------ | ---------- | ---------- | --------------------- |
| - [^.*$](#interface_pattern1 ) | Yes     | object | No         | -          | Name of the interface |

### <a name="interface_pattern1"></a>1.1. Pattern Property `Data Collection Service Module Config Schema > interface > ^.*$`
> All properties whose name matches the regular expression
```^.*$``` ([Test](https://regex101.com/?regex=%5E.%2A%24))
must respect the following conditions

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Name of the interface

| Property                                | Pattern | Type   | Deprecated | Definition | Title/Description                                  |
| --------------------------------------- | ------- | ------ | ---------- | ---------- | -------------------------------------------------- |
| + [module](#interface_pattern1_module ) | No      | string | No         | -          | Name / path of the interface module to import      |
| + [class](#interface_pattern1_class )   | No      | string | No         | -          | Name of the interface class to use                 |
| - [config](#interface_pattern1_config ) | No      | object | No         | -          | Additional config specific to the interface module |

#### <a name="interface_pattern1_module"></a>1.1.1. Property `Data Collection Service Module Config Schema > interface > ^.*$ > module`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Name / path of the interface module to import

#### <a name="interface_pattern1_class"></a>1.1.2. Property `Data Collection Service Module Config Schema > interface > ^.*$ > class`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Name of the interface class to use

#### <a name="interface_pattern1_config"></a>1.1.3. Property `Data Collection Service Module Config Schema > interface > ^.*$ > config`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Additional config specific to the interface module

## <a name="device"></a>2. Property `Data Collection Service Module Config Schema > device`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Set of devices

| Property                    | Pattern | Type   | Deprecated | Definition | Title/Description  |
| --------------------------- | ------- | ------ | ---------- | ---------- | ------------------ |
| - [^.*$](#device_pattern1 ) | Yes     | object | No         | -          | Name of the device |

### <a name="device_pattern1"></a>2.1. Pattern Property `Data Collection Service Module Config Schema > device > ^.*$`
> All properties whose name matches the regular expression
```^.*$``` ([Test](https://regex101.com/?regex=%5E.%2A%24))
must respect the following conditions

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Name of the device

| Property                                   | Pattern | Type   | Deprecated | Definition | Title/Description                                                                              |
| ------------------------------------------ | ------- | ------ | ---------- | ---------- | ---------------------------------------------------------------------------------------------- |
| + [module](#device_pattern1_module )       | No      | string | No         | -          | Name / path of the device module to import                                                     |
| + [class](#device_pattern1_class )         | No      | string | No         | -          | Name of the device class to use                                                                |
| - [interface](#device_pattern1_interface ) | No      | string | No         | -          | Name of the interface this device uses                                                         |
| - [config](#device_pattern1_config )       | No      | object | No         | -          | Additional config specific to the device module                                                |
| + [variables](#device_pattern1_variables ) | No      | object | No         | -          | Links the inputs and outputs of the module to named variables on its sensing stacks blackboard |

#### <a name="device_pattern1_module"></a>2.1.1. Property `Data Collection Service Module Config Schema > device > ^.*$ > module`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Name / path of the device module to import

#### <a name="device_pattern1_class"></a>2.1.2. Property `Data Collection Service Module Config Schema > device > ^.*$ > class`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Name of the device class to use

#### <a name="device_pattern1_interface"></a>2.1.3. Property `Data Collection Service Module Config Schema > device > ^.*$ > interface`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Name of the interface this device uses

#### <a name="device_pattern1_config"></a>2.1.4. Property `Data Collection Service Module Config Schema > device > ^.*$ > config`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Additional config specific to the device module

#### <a name="device_pattern1_variables"></a>2.1.5. Property `Data Collection Service Module Config Schema > device > ^.*$ > variables`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Links the inputs and outputs of the module to named variables on its sensing stacks blackboard

## <a name="calculation"></a>3. Property `Data Collection Service Module Config Schema > calculation`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Set of calculations

| Property                         | Pattern | Type   | Deprecated | Definition | Title/Description       |
| -------------------------------- | ------- | ------ | ---------- | ---------- | ----------------------- |
| - [^.*$](#calculation_pattern1 ) | Yes     | object | No         | -          | Name of the calculation |

### <a name="calculation_pattern1"></a>3.1. Pattern Property `Data Collection Service Module Config Schema > calculation > ^.*$`
> All properties whose name matches the regular expression
```^.*$``` ([Test](https://regex101.com/?regex=%5E.%2A%24))
must respect the following conditions

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Name of the calculation

| Property                                        | Pattern | Type   | Deprecated | Definition | Title/Description                                                                              |
| ----------------------------------------------- | ------- | ------ | ---------- | ---------- | ---------------------------------------------------------------------------------------------- |
| + [module](#calculation_pattern1_module )       | No      | string | No         | -          | Name / path of the calculation module to import                                                |
| + [class](#calculation_pattern1_class )         | No      | string | No         | -          | Name of the calculation class to use                                                           |
| - [config](#calculation_pattern1_config )       | No      | object | No         | -          | Additional config specific to the calculation module                                           |
| + [variables](#calculation_pattern1_variables ) | No      | object | No         | -          | Links the inputs and outputs of the module to named variables on its sensing stacks blackboard |

#### <a name="calculation_pattern1_module"></a>3.1.1. Property `Data Collection Service Module Config Schema > calculation > ^.*$ > module`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Name / path of the calculation module to import

#### <a name="calculation_pattern1_class"></a>3.1.2. Property `Data Collection Service Module Config Schema > calculation > ^.*$ > class`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Name of the calculation class to use

#### <a name="calculation_pattern1_config"></a>3.1.3. Property `Data Collection Service Module Config Schema > calculation > ^.*$ > config`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Additional config specific to the calculation module

#### <a name="calculation_pattern1_variables"></a>3.1.4. Property `Data Collection Service Module Config Schema > calculation > ^.*$ > variables`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Links the inputs and outputs of the module to named variables on its sensing stacks blackboard

## <a name="pipelines"></a>4. Property `Data Collection Service Module Config Schema > pipelines`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Specifies one or more calculation pipelines that can be used in sensing stacks

| Property                       | Pattern | Type            | Deprecated | Definition | Title/Description    |
| ------------------------------ | ------- | --------------- | ---------- | ---------- | -------------------- |
| - [^.*$](#pipelines_pattern1 ) | Yes     | array of string | No         | -          | Name of the pipeline |

### <a name="pipelines_pattern1"></a>4.1. Pattern Property `Data Collection Service Module Config Schema > pipelines > ^.*$`
> All properties whose name matches the regular expression
```^.*$``` ([Test](https://regex101.com/?regex=%5E.%2A%24))
must respect the following conditions

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |

**Description:** Name of the pipeline

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be         | Description                                             |
| --------------------------------------- | ------------------------------------------------------- |
| [^.*$ items](#pipelines_pattern1_items) | List of calculations in the pipeline (in reverse order) |

#### <a name="pipelines_pattern1_items"></a>4.1.1. Data Collection Service Module Config Schema > pipelines > ^.*$ > ^.*$ items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** List of calculations in the pipeline (in reverse order)

## <a name="measurement"></a>5. Property `Data Collection Service Module Config Schema > measurement`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Specifies the measurement policy for the service module

| Property                                         | Pattern | Type            | Deprecated | Definition | Title/Description                           |
| ------------------------------------------------ | ------- | --------------- | ---------- | ---------- | ------------------------------------------- |
| + [module](#measurement_module )                 | No      | string          | No         | -          | Name / path of the module to import         |
| + [class](#measurement_class )                   | No      | string          | No         | -          | Name of the class to use                    |
| - [config](#measurement_config )                 | No      | object          | No         | -          | Additional config for the chosen class      |
| + [sensing_stacks](#measurement_sensing_stacks ) | No      | array of object | No         | -          | List of sensing stacks for this measurement |

### <a name="measurement_module"></a>5.1. Property `Data Collection Service Module Config Schema > measurement > module`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Name / path of the module to import

### <a name="measurement_class"></a>5.2. Property `Data Collection Service Module Config Schema > measurement > class`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Name of the class to use

### <a name="measurement_config"></a>5.3. Property `Data Collection Service Module Config Schema > measurement > config`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Additional config for the chosen class

### <a name="measurement_sensing_stacks"></a>5.4. Property `Data Collection Service Module Config Schema > measurement > sensing_stacks`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** List of sensing stacks for this measurement

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                           | Description |
| --------------------------------------------------------- | ----------- |
| [sensing_stacks items](#measurement_sensing_stacks_items) | -           |

#### <a name="measurement_sensing_stacks_items"></a>5.4.1. Data Collection Service Module Config Schema > measurement > sensing_stacks > sensing_stacks items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                                    | Pattern | Type   | Deprecated | Definition | Title/Description                                                 |
| ----------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------------------------------------------------------- |
| + [device](#measurement_sensing_stacks_items_device )       | No      | string | No         | -          | Device sampled for this sensing stack                             |
| + [pipeline](#measurement_sensing_stacks_items_pipeline )   | No      | string | No         | -          | Calculation pipeline applied to the sample                        |
| - [constants](#measurement_sensing_stacks_items_constants ) | No      | object | No         | -          | Additional constants to add to the output from this sensing stack |
| - [prefix](#measurement_sensing_stacks_items_prefix )       | No      | string | No         | -          | prefix to add to all variables output from this sensing stack     |

##### <a name="measurement_sensing_stacks_items_device"></a>5.4.1.1. Property `Data Collection Service Module Config Schema > measurement > sensing_stacks > sensing_stacks items > device`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Device sampled for this sensing stack

##### <a name="measurement_sensing_stacks_items_pipeline"></a>5.4.1.2. Property `Data Collection Service Module Config Schema > measurement > sensing_stacks > sensing_stacks items > pipeline`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Calculation pipeline applied to the sample

##### <a name="measurement_sensing_stacks_items_constants"></a>5.4.1.3. Property `Data Collection Service Module Config Schema > measurement > sensing_stacks > sensing_stacks items > constants`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Additional constants to add to the output from this sensing stack

##### <a name="measurement_sensing_stacks_items_prefix"></a>5.4.1.4. Property `Data Collection Service Module Config Schema > measurement > sensing_stacks > sensing_stacks items > prefix`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** prefix to add to all variables output from this sensing stack

## <a name="output"></a>6. Property `Data Collection Service Module Config Schema > output`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Specifies the outputs from this service module

| Property                    | Pattern | Type   | Deprecated | Definition | Title/Description  |
| --------------------------- | ------- | ------ | ---------- | ---------- | ------------------ |
| - [^.*$](#output_pattern1 ) | Yes     | object | No         | -          | name of the output |

### <a name="output_pattern1"></a>6.1. Pattern Property `Data Collection Service Module Config Schema > output > ^.*$`
> All properties whose name matches the regular expression
```^.*$``` ([Test](https://regex101.com/?regex=%5E.%2A%24))
must respect the following conditions

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** name of the output

| Property                                         | Pattern | Type   | Deprecated | Definition | Title/Description                                          |
| ------------------------------------------------ | ------- | ------ | ---------- | ---------- | ---------------------------------------------------------- |
| + [topic](#output_pattern1_topic )               | No      | string | No         | -          | Topic to publish this output on (must be valid MQTT topic) |
| + [message_spec](#output_pattern1_message_spec ) | No      | object | No         | -          | Message specification for this output                      |

#### <a name="output_pattern1_topic"></a>6.1.1. Property `Data Collection Service Module Config Schema > output > ^.*$ > topic`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Topic to publish this output on (must be valid MQTT topic)

| Restrictions                      |                                                                                                                                         |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^([^#+$/]*/?)+[^#+$/]*$``` [Test](https://regex101.com/?regex=%5E%28%5B%5E%23%2B%24%2F%5D%2A%2F%3F%29%2B%5B%5E%23%2B%24%2F%5D%2A%24) |

#### <a name="output_pattern1_message_spec"></a>6.1.2. Property `Data Collection Service Module Config Schema > output > ^.*$ > message_spec`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Message specification for this output

## <a name="mqtt"></a>7. Property `Data Collection Service Module Config Schema > mqtt`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Contains the configuration for the MQTT client

| Property                              | Pattern | Type    | Deprecated | Definition | Title/Description                                        |
| ------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------------------------------------------- |
| + [broker](#mqtt_broker )             | No      | string  | No         | -          | URL of the mqtt broker                                   |
| + [port](#mqtt_port )                 | No      | integer | No         | -          | Port to use when connecting to the broker                |
| - [topic_prefix](#mqtt_topic_prefix ) | No      | string  | No         | -          | prefix to prepend to the topic of all published messages |
| - [reconnect](#mqtt_reconnect )       | No      | object  | No         | -          | Reconnect characteristics                                |

### <a name="mqtt_broker"></a>7.1. Property `Data Collection Service Module Config Schema > mqtt > broker`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** URL of the mqtt broker

### <a name="mqtt_port"></a>7.2. Property `Data Collection Service Module Config Schema > mqtt > port`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** Port to use when connecting to the broker

### <a name="mqtt_topic_prefix"></a>7.3. Property `Data Collection Service Module Config Schema > mqtt > topic_prefix`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** prefix to prepend to the topic of all published messages

### <a name="mqtt_reconnect"></a>7.4. Property `Data Collection Service Module Config Schema > mqtt > reconnect`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Reconnect characteristics

| Property                              | Pattern | Type    | Deprecated | Definition | Title/Description                                                |
| ------------------------------------- | ------- | ------- | ---------- | ---------- | ---------------------------------------------------------------- |
| - [initial](#mqtt_reconnect_initial ) | No      | number  | No         | -          | Initial delay before attempting to reconnect (in seconds)        |
| - [backoff](#mqtt_reconnect_backoff ) | No      | number  | No         | -          | Multiplier by which the delay increases on each failed reconnect |
| - [limit](#mqtt_reconnect_limit )     | No      | integer | No         | -          | Upper limit on the delay between reconnect attempts (in seconds) |

#### <a name="mqtt_reconnect_initial"></a>7.4.1. Property `Data Collection Service Module Config Schema > mqtt > reconnect > initial`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

**Description:** Initial delay before attempting to reconnect (in seconds)

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

#### <a name="mqtt_reconnect_backoff"></a>7.4.2. Property `Data Collection Service Module Config Schema > mqtt > reconnect > backoff`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

**Description:** Multiplier by which the delay increases on each failed reconnect

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 1 |

#### <a name="mqtt_reconnect_limit"></a>7.4.3. Property `Data Collection Service Module Config Schema > mqtt > reconnect > limit`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

**Description:** Upper limit on the delay between reconnect attempts (in seconds)

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-05-22 at 12:45:25 +0100
