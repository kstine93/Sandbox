#Make API request adding a new request to the system:
curl -X POST -H "Content-Type: application/json" localhost:8000/api/v1/requests/new \
-d '{"requests":[{"email":"test@email.de","request_cause":"direct_request"},{"email":"test2@email.de","request_cause":"direct_request"}]}'