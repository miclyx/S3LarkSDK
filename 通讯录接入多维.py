      
import lark_oapi as lark
from lark_oapi.api.contact.v3 import FindByDepartmentUserResponse, FindByDepartmentUserRequest
from lark_oapi.api.bitable.v1 import AppTableRecord, BatchCreateAppTableRecordRequest, BatchCreateAppTableRecordRequestBody

def main():
    client = lark.Client.builder() \
        .app_id("cli_a6c1c8a4cd3b500e") \
        .app_secret("UlSdEhKmxfVag2YCpMXu0gRednVoonPm") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    request = FindByDepartmentUserRequest.builder() \
        .user_id_type("user_id") \
        .department_id_type("department_id") \
        .department_id("7efb97cg31g9dge1") \
        .page_size(50) \
        .page_token("") \
        .build()

    response = client.contact.v3.user.find_by_department(request)

    if response.success():
        records = []
        for user in response.data.items:
            record = AppTableRecord.builder() \
                .fields({
                "姓名": user.name,
                "邮箱": user.email,
                "手机号": user.mobile,
                "职位": user.job_title,
                "department_ids": user.department_ids,
                "enterprise_email": user.enterprise_email,
                "open_id": user.open_id,
                "union_id": user.union_id,
                "user_id": user.user_id,
            }) \
                .build()
            records.append(record)

        bitable_request = BatchCreateAppTableRecordRequest.builder() \
            .app_token("Ps4ybl8LEaEAxNs4eO8csXj1nCd") \
            .table_id("tbl1fLQUIqrRZYh1") \
            .request_body(BatchCreateAppTableRecordRequestBody.builder() \
                          .records(records) \
                          .build()) \
            .build()


        bitable_response = client.bitable.v1.app_table_record.batch_create(bitable_request)

        if not bitable_response.success():
            lark.logger.error(
                f"Batch create failed, code: {bitable_response.code}, msg: {bitable_response.msg}, log_id: {bitable_response.get_log_id()}")
            return

        lark.logger.info(
            f"Records successfully created in Bitable: {lark.JSON.marshal(bitable_response.data, indent=4)}")

if __name__ == "__main__":
    main()

    
