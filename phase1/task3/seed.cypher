// Clear existing data so this script is safely re-runnable.
MATCH (n) DETACH DELETE n;

// 6 Person nodes with name, age, city.
CREATE (alice:Person {name: 'Alice', age: 29, city: 'New York'});
CREATE (bob:Person {name: 'Bob', age: 34, city: 'Boston'});
CREATE (carol:Person {name: 'Carol', age: 27, city: 'New York'});
CREATE (dave:Person {name: 'Dave', age: 41, city: 'Chicago'});
CREATE (erin:Person {name: 'Erin', age: 23, city: 'Boston'});
CREATE (frank:Person {name: 'Frank', age: 38, city: 'Chicago'});

// 11 FOLLOWS relationships (>= 8 required).
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[:FOLLOWS]->(b);
MATCH (a:Person {name: 'Alice'}), (c:Person {name: 'Carol'})
CREATE (a)-[:FOLLOWS]->(c);
MATCH (a:Person {name: 'Alice'}), (d:Person {name: 'Dave'})
CREATE (a)-[:FOLLOWS]->(d);
MATCH (b:Person {name: 'Bob'}), (d:Person {name: 'Dave'})
CREATE (b)-[:FOLLOWS]->(d);
MATCH (b:Person {name: 'Bob'}), (e:Person {name: 'Erin'})
CREATE (b)-[:FOLLOWS]->(e);
MATCH (c:Person {name: 'Carol'}), (d:Person {name: 'Dave'})
CREATE (c)-[:FOLLOWS]->(d);
MATCH (c:Person {name: 'Carol'}), (f:Person {name: 'Frank'})
CREATE (c)-[:FOLLOWS]->(f);
MATCH (e:Person {name: 'Erin'}), (d:Person {name: 'Dave'})
CREATE (e)-[:FOLLOWS]->(d);
MATCH (f:Person {name: 'Frank'}), (d:Person {name: 'Dave'})
CREATE (f)-[:FOLLOWS]->(d);
MATCH (e:Person {name: 'Erin'}), (b:Person {name: 'Bob'})
CREATE (e)-[:FOLLOWS]->(b);
MATCH (f:Person {name: 'Frank'}), (c:Person {name: 'Carol'})
CREATE (f)-[:FOLLOWS]->(c);

// 4 Post nodes with content and timestamp, each POSTED by a person.
MATCH (a:Person {name: 'Alice'})
CREATE (a)-[:POSTED]->(:Post {content: 'Excited to start this new project!', timestamp: datetime('2026-07-01T09:00:00')});
MATCH (b:Person {name: 'Bob'})
CREATE (b)-[:POSTED]->(:Post {content: 'Great hike in the mountains today.', timestamp: datetime('2026-07-15T18:30:00')});
MATCH (d:Person {name: 'Dave'})
CREATE (d)-[:POSTED]->(:Post {content: 'Just published a new blog post on graph databases.', timestamp: datetime('2026-07-20T11:15:00')});
MATCH (f:Person {name: 'Frank'})
CREATE (f)-[:POSTED]->(:Post {content: 'Coffee tastes better on rainy days.', timestamp: datetime('2026-08-01T08:00:00')});
