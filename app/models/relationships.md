## One-to-many Relationship
There are cases where the duplication that occurs when storing secondary data in the
same table as the primary entity is a problem. This is because the table may grow much
larger than it needs to be and variation in the spelling of duplicated data can produce
incorrectly grouped results. When you find that information is being duplicated, consider
defining the entity with its own table.

1. state-to-plan: there are many plans for a given state
2. metal-level-to-plan: a metal level can have multiple plans
3. rate-to-plan: this is actually a one-to-one relationship (which is a special kind of one-to-many relationship) because there is only one rate for each plan
4. rate-area-to-plan: one rate area can have many plans
5. state-to-zipcode: a state can have many zip codes
6. state-to-county-code: a state can have many county codes
7. state-to-county-name: a state can have many county names
8. zipcode-to-rate-area: a zipcode can have multiple rate areas (which would make the SLCSP indeterminable but that calculation is made in the application logic)
9. rate-area-to-zipcode: a rate area can have more than one zipcode
10. state-to-rate-area: this is another one-to-one relationship

## Database Tables

1. States should be in a table with relationships to zipcodes, counties, county codes, rate areas, metal levels, and plans. The state has the name and abbreviation
2. Plans should be in a table containing the plan_id and the rate
3. Metal levels should be in a table
4. Rate areas should be in a table
5. zipcodes are in their own table



