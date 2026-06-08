Process a newly written scene: index it, draft knowledge deltas, and update the knowledge graph.

Process a new or updated scene file and update the knowledge graph.

Steps:
1. Ask for the scene file path and chapter number if not provided.
2. Call `process_new_scene` MCP tool.
3. Show the draft knowledge deltas as a diff for approval.
4. On approval: confirm git commit.
5. Show inversion test results for this scene.
6. Note any failures: "N tests failed — consider running /sync to re-check or /exportdb to checkpoint."
