# Updating Generated Docs
## Recipe schema
### Setup
```
pipx install json-schema-for-humans
```
### Generation
```
generate-schema-doc --config template_name=md ../code/config_schema.json ./recipe_schema/recipe_schema.md
```
```
generate-schema-doc --config template_name=js ../code/config_schema.json ./recipe_schema/recipe_schema.html
```