from test_utils import test_request

baseUrl = "/api/v1/requests"
baseHeader = {"Content-Type":"application/json"}


#Small wrapper functions to reduce repetition:
#--------------------
def test_post(url: str, **request_args):
    return test_request(method="POST"
                        ,url=url
                        ,headers=baseHeader
                        ,**request_args)

#--------------------
def test_get(url: str, **request_args):
    return test_request(method="GET"
                        ,url=url
                        ,**request_args)

#-----------------------
#---Finished Requests---
#-----------------------

def test_finishedRequests_noDates_normal(api_host: str):
    return test_post(
        url=f"{api_host}{baseUrl}/finished"
    )

def test_finishedRequests_emptyDates_normal(api_host: str):
    return test_post(
        url=f"{api_host}{baseUrl}/finished"
        ,body={}
    )

def test_finishedRequests_withDates_normal(api_host: str):
    return test_post(
        url=f"{api_host}{baseUrl}/finished"
        ,body={"startDate":"2022-01-01","endDate":"2023-12-30"}
    )

def test_finishedRequests_withDates_reversedDateFormat(api_host: str):
    return test_post(
        url=f"{api_host}{baseUrl}/finished"
        ,body={"startDate":"01-01-2022","endDate":"12-30-2022"}
    )

def test_finishedRequests_withDates_onlyStartDate(api_host: str):
    return test_post(
        url=f"{api_host}{baseUrl}/finished"
        ,body={"startDate":"2022-01-01"}
    )

def test_finishedRequests_withDates_onlyEndDate(api_host: str):
    return test_post(
        url=f"{api_host}{baseUrl}/finished"
        ,body={"endDate":"2023-12-30"}
    )

def test_finishedRequests_withDates_misnamedField(api_host: str):
    return test_post(
        url=f"{api_host}{baseUrl}/finished"
        ,body={"wrongDate":"2022-01-01"}
    )

#------------------
#---New Requests---
#------------------
def test_newRequest_normal(api_host: str):
    return test_post(
        url=f"{api_host}{baseUrl}/new"
        ,body={"requests":[{"email":"test@email.de","request_cause":"direct_request"}]}
    )

def test_newRequest_bulk(api_host: str,count: int=100):
    entries = [{"email":f"em_{i}@test.de","request_cause":"direct_request"} for i in range(1,count)]
    return test_post(
        url=f"{api_host}{baseUrl}/new"
        ,body={"requests":entries}
    )

def test_newRequest_allCauses(api_host: str):
    return test_post(
        url=f"{api_host}{baseUrl}/new"
        ,body={"requests":[
            {"email":"test@email.de","request_cause":"direct_request"}
            ,{"email":"test2@email.de","request_cause":"account_deleted"}
            ,{"email":"test3@email.de","request_cause":"email_opt_out"}
            ,{"email":"test4@email.de","request_cause":"inactive"}
            ,{"email":"test5@email.de","request_cause":"other"}
        ]}
    )

def test_newRequest_blankEmail(api_host: str):
    return test_post(
        url=f"{api_host}{baseUrl}/new"
        ,body={"requests":[{"email":" ","request_cause":"direct_request"}]}
    )

def test_newRequest_blankCause(api_host: str):
    return test_post(
        url=f"{api_host}{baseUrl}/new"
        ,body={"requests":[{"email":"test@email.de","request_cause":" "}]}
    )

def test_newRequest_misnamedField(api_host: str):
    return test_post(
        url=f"{api_host}{baseUrl}/new"
        ,body={"requests":[{"email":"test@email.de","wrong_cause":"direct_request"}]}
    )

def test_newRequest_extraField(api_host: str):
    return test_post(
        url=f"{api_host}{baseUrl}/new"
        ,body={"requests":[{"email":"test@email.de","request_cause":"direct_request","injection":"BAD STUFF"}]}
    )

def test_newRequest_missingCause(api_host: str):
    return test_post(
        url=f"{api_host}{baseUrl}/new"
        ,body={"requests":[{"email":"test@email.de"}]}
    )

#----------------------
#---Pending Requests---
#----------------------
def test_pendingRequests_get_normal(api_host: str):
    return test_get(
        url=f"{api_host}{baseUrl}/pending"
    )

def test_pendingRequests_approve_id(api_host: str, id: int = 1):
    return test_post(
        url=f"{api_host}{baseUrl}/pending/{id}"
        ,body={"rejected":True}
    )

def test_pendingRequests_reject_id(api_host: str, id: int = 1):
    return test_post(
        url=f"{api_host}{baseUrl}/pending/{id}"
        ,body={"rejected":False}
    )

def test_pendingRequests_change_cause(api_host: str, id: int = 1):
    return test_post(
        url=f"{api_host}{baseUrl}/pending/{id}"
        ,body={"request_cause":"direct_request"}
    )

def test_pendingRequests_rejectedAsString(api_host: str, id: int = 1):
    return test_post(
        url=f"{api_host}{baseUrl}/pending/{id}"
        ,body={"rejected":"True"}
    )

def test_pendingRequests_wrongId(api_host: str):
    return test_post(
        url=f"{api_host}{baseUrl}/pending/-1"
        ,body={"rejected":"False"}
    )

def test_pendingRequests_invalidCause(api_host: str, id: int = 1):
    return test_post(
        url=f"{api_host}{baseUrl}/pending/{id}"
        ,body={"request_cause":"invalid cause!"}
    )

def test_pendingRequests_misnamedField(api_host: str, id: int = 1):
    return test_post(
        url=f"{api_host}{baseUrl}/pending/{id}"
        ,body={"mIsNaMeD_FiElD":"True"}
    )

def test_pendingRequests_emptyBody(api_host: str, id: int = 1):
    return test_post(
        url=f"{api_host}{baseUrl}/pending/{id}"
        ,body={}
    )