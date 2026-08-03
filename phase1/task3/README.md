# Task C — Neo4j Cypher Query Set

A simple social network graph and the required Cypher queries.

## Files
- `seed.cypher` — 6 `Person` nodes, 11 `FOLLOWS` relationships, 4 `Post` nodes linked via `POSTED`
- `queries.cypher` — the 3 required queries

## Graph model
```
(:Person {name, age, city})
(:Post {content, timestamp})
(:Person)-[:FOLLOWS]->(:Person)
(:Person)-[:POSTED]->(:Post)
```

## Running it

### Neo4j sandbox
Open [sandbox.neo4j.com](https://sandbox.neo4j.com), create a "Blank Sandbox," open the Neo4j Browser, and paste the contents of `seed.cypher` then `queries.cypher` into the query editor.

### Local Neo4j (Docker)
```bash
docker run -d --name social_graph -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/yourpassword neo4j:5-community

cypher-shell -u neo4j -p yourpassword -f seed.cypher
cypher-shell -u neo4j -p yourpassword -f queries.cypher
```
`seed.cypher` starts with `MATCH (n) DETACH DELETE n;`, so it can be re-run safely against an empty or previously-seeded database.

## The network
People: Alice, Bob, Carol, Dave, Erin, Frank (with `age` and `city`).

Follows: Alice → {Bob, Carol, Dave}; Bob → {Dave, Erin}; Carol → {Dave, Frank}; Erin → {Dave, Bob}; Frank → {Dave, Carol}. Dave has no outgoing follows, making him the most-followed node — this exercises query 3's ranking.

Posts: one each from Alice, Bob, Dave, and Frank, with `content` and a `timestamp`.

## Queries
1. **All people Alice follows.**
2. **Friends-of-friends** — people followed by someone Alice follows, excluding people Alice already follows (and Alice herself).
3. **Top 3 most followed people**, by count of incoming `FOLLOWS` relationships.

## Verified output
Run against a live Neo4j 5 (community) instance:

1. Dave, Carol, Bob (Alice's direct follows).
2. Frank, Erin (followed by Bob/Carol, but not already followed by Alice).
3. Dave (5), Bob (2), Carol (2).

## AI-Generated Parts
This graph model and query set were generated with Claude (Anthropic), then verified by running them against a live Neo4j (Docker) instance to confirm each result is correct.
