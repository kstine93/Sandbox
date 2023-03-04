from endpoint_calls import *
import configparser

config = configparser.ConfigParser()
config.read('../deletion_app.cfg')
#api_host = config['API_SPECS']['api_host'] + ":" + config['API_SPECS']['api_port']
api_host = "192.168.49.2:30004"
#--------------------
#---Test Scenarios---
#--------------------

#1. Normal requests:

assert test_newRequest_normal(api_host).status == 200
assert test_newRequest_allCauses(api_host).status == 200
assert test_newRequest_bulk(api_host).status == 200

assert test_pendingRequests_get_normal(api_host).status == 200
assert test_pendingRequests_approve_id(api_host, id = 1).status == 200
assert test_pendingRequests_reject_id(api_host, id = 1).status == 200
assert test_pendingRequests_rejectedAsString(api_host, id = 1).status == 200
assert test_pendingRequests_change_cause(api_host, id = 1).status == 200

assert test_finishedRequests_noDates_normal(api_host).status == 200
assert test_finishedRequests_withDates_normal(api_host).status == 200
assert test_finishedRequests_emptyDates_normal(api_host).status == 200
assert test_finishedRequests_withDates_onlyEndDate(api_host).status == 200
assert test_finishedRequests_withDates_onlyStartDate(api_host).status == 200

print("-------------------------------")
print("--Passed normal request tests--")
print("-------------------------------")

#2. Bad requests:
assert test_newRequest_misnamedField(api_host).status == 422
assert test_newRequest_extraField(api_host).status == 422
assert test_newRequest_blankCause(api_host).status == 422
assert test_newRequest_missingCause(api_host).status == 422
assert test_newRequest_blankEmail(api_host).status == 422

assert test_pendingRequests_wrongId(api_host).status == 400
assert test_pendingRequests_invalidCause(api_host).status == 422
assert test_pendingRequests_misnamedField(api_host).status == 422
assert test_pendingRequests_emptyBody(api_host).status == 422

assert test_finishedRequests_withDates_misnamedField(api_host).status == 422
assert test_finishedRequests_withDates_reversedDateFormat(api_host).status == 422

print("----------------------------")
print("--Passed bad request tests--")
print("----------------------------")

print("======================")
print("== ALL TESTS PASSED ==")
print("======================")