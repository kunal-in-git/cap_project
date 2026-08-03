// =====================================================================
// Query 1: Find all people that a specific person (e.g. 'Alice') follows.
// =====================================================================
MATCH (p:Person {name: 'Alice'})-[:FOLLOWS]->(followed:Person)
RETURN followed.name AS name, followed.age AS age, followed.city AS city;


// =====================================================================
// Query 2: Friends-of-friends — people followed by someone Alice
// follows, that Alice does not already follow (and excluding Alice
// herself).
// =====================================================================
MATCH (alice:Person {name: 'Alice'})-[:FOLLOWS]->(:Person)-[:FOLLOWS]->(fof:Person)
WHERE NOT (alice)-[:FOLLOWS]->(fof)
  AND fof <> alice
RETURN DISTINCT fof.name AS name, fof.age AS age, fof.city AS city;


// =====================================================================
// Query 3: Find the 3 most followed people in the network (by count
// of incoming FOLLOWS relationships).
// =====================================================================
MATCH (p:Person)<-[:FOLLOWS]-()
RETURN p.name AS name, count(*) AS follower_count
ORDER BY follower_count DESC, p.name ASC
LIMIT 3;
