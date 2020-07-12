# mock8s
Easily mock tests from kubernetes-client

## Support

### CoreV1Api
|method|supported?|
|---|---|
|`connect_delete_namespaced_pod_proxy`|:x:|
|`connect_delete_namespaced_pod_proxy_with_path`|:x:|
|`connect_delete_namespaced_service_proxy`|:x:|
|`connect_delete_namespaced_service_proxy_with_path`|:x:|
|`connect_delete_node_proxy`|:x:|
|`connect_delete_node_proxy_with_path`|:x:|
|`connect_get_namespaced_pod_attach`|:x:|
|`connect_get_namespaced_pod_exec`|:x:|
|`connect_get_namespaced_pod_portforward`|:x:|
|`connect_get_namespaced_pod_proxy`|:x:|
|`connect_get_namespaced_pod_proxy_with_path`|:x:|
|`connect_get_namespaced_service_proxy`|:x:|
|`connect_get_namespaced_service_proxy_with_path`|:x:|
|`connect_get_node_proxy`|:x:|
|`connect_get_node_proxy_with_path`|:x:|
|`connect_head_namespaced_pod_proxy`|:x:|
|`connect_head_namespaced_pod_proxy_with_path`|:x:|
|`connect_head_namespaced_service_proxy`|:x:|
|`connect_head_namespaced_service_proxy_with_path`|:x:|
|`connect_head_node_proxy`|:x:|
|`connect_head_node_proxy_with_path`|:x:|
|`connect_options_namespaced_pod_proxy`|:x:|
|`connect_options_namespaced_pod_proxy_with_path`|:x:|
|`connect_options_namespaced_service_proxy`|:x:|
|`connect_options_namespaced_service_proxy_with_path`|:x:|
|`connect_options_node_proxy`|:x:|
|`connect_options_node_proxy_with_path`|:x:|
|`connect_patch_namespaced_pod_proxy`|:x:|
|`connect_patch_namespaced_pod_proxy_with_path`|:x:|
|`connect_patch_namespaced_service_proxy`|:x:|
|`connect_patch_namespaced_service_proxy_with_path`|:x:|
|`connect_patch_node_proxy`|:x:|
|`connect_patch_node_proxy_with_path`|:x:|
|`connect_post_namespaced_pod_attach`|:x:|
|`connect_post_namespaced_pod_exec`|:x:|
|`connect_post_namespaced_pod_portforward`|:x:|
|`connect_post_namespaced_pod_proxy`|:x:|
|`connect_post_namespaced_pod_proxy_with_path`|:x:|
|`connect_post_namespaced_service_proxy`|:x:|
|`connect_post_namespaced_service_proxy_with_path`|:x:|
|`connect_post_node_proxy`|:x:|
|`connect_post_node_proxy_with_path`|:x:|
|`connect_put_namespaced_pod_proxy`|:x:|
|`connect_put_namespaced_pod_proxy_with_path`|:x:|
|`connect_put_namespaced_service_proxy`|:x:|
|`connect_put_namespaced_service_proxy_with_path`|:x:|
|`connect_put_node_proxy`|:x:|
|`connect_put_node_proxy_with_path`|:x:|
|`create_namespace`|:x:|
|`create_namespaced_binding`|:x:|
|`create_namespaced_config_map`|:x:|
|`create_namespaced_endpoints`|:x:|
|`create_namespaced_event`|:x:|
|`create_namespaced_limit_range`|:x:|
|`create_namespaced_persistent_volume_claim`|:x:|
|`create_namespaced_pod`|:white_check_mark:|
|`create_namespaced_pod_binding`|:x:|
|`create_namespaced_pod_eviction`|:x:|
|`create_namespaced_pod_template`|:x:|
|`create_namespaced_replication_controller`|:x:|
|`create_namespaced_resource_quota`|:x:|
|`create_namespaced_secret`|:x:|
|`create_namespaced_service`|:white_check_mark:|
|`create_namespaced_service_account`|:x:|
|`create_namespaced_service_account_token`|:x:|
|`create_node`|:x:|
|`create_persistent_volume`|:x:|
|`delete_collection_namespaced_config_map`|:x:|
|`delete_collection_namespaced_endpoints`|:x:|
|`delete_collection_namespaced_event`|:x:|
|`delete_collection_namespaced_limit_range`|:x:|
|`delete_collection_namespaced_persistent_volume_claim`|:x:|
|`delete_collection_namespaced_pod`|:x:|
|`delete_collection_namespaced_pod_template`|:x:|
|`delete_collection_namespaced_replication_controller`|:x:|
|`delete_collection_namespaced_resource_quota`|:x:|
|`delete_collection_namespaced_secret`|:x:|
|`delete_collection_namespaced_service_account`|:x:|
|`delete_collection_node`|:x:|
|`delete_collection_persistent_volume`|:x:|
|`delete_namespace`|:x:|
|`delete_namespaced_config_map`|:x:|
|`delete_namespaced_endpoints`|:x:|
|`delete_namespaced_event`|:x:|
|`delete_namespaced_limit_range`|:x:|
|`delete_namespaced_persistent_volume_claim`|:x:|
|`delete_namespaced_pod`|:white_check_mark:|
|`delete_namespaced_pod_template`|:x:|
|`delete_namespaced_replication_controller`|:x:|
|`delete_namespaced_resource_quota`|:x:|
|`delete_namespaced_secret`|:x:|
|`delete_namespaced_service`|:white_check_mark:|
|`delete_namespaced_service_account`|:x:|
|`delete_node`|:x:|
|`delete_persistent_volume`|:x:|
|`get_api_resources`|:x:|
|`list_component_status`|:x:|
|`list_config_map_for_all_namespaces`|:x:|
|`list_endpoints_for_all_namespaces`|:x:|
|`list_event_for_all_namespaces`|:x:|
|`list_limit_range_for_all_namespaces`|:x:|
|`list_namespace`|:x:|
|`list_namespaced_config_map`|:x:|
|`list_namespaced_endpoints`|:x:|
|`list_namespaced_event`|:x:|
|`list_namespaced_limit_range`|:x:|
|`list_namespaced_persistent_volume_claim`|:x:|
|`list_namespaced_pod`|:white_check_mark:|
|`list_namespaced_pod_template`|:x:|
|`list_namespaced_replication_controller`|:x:|
|`list_namespaced_resource_quota`|:x:|
|`list_namespaced_secret`|:x:|
|`list_namespaced_service`|:white_check_mark:|
|`list_namespaced_service_account`|:x:|
|`list_node`|:x:|
|`list_persistent_volume`|:x:|
|`list_persistent_volume_claim_for_all_namespaces`|:x:|
|`list_pod_for_all_namespaces`|:white_check_mark:|
|`list_pod_template_for_all_namespaces`|:x:|
|`list_replication_controller_for_all_namespaces`|:x:|
|`list_resource_quota_for_all_namespaces`|:x:|
|`list_secret_for_all_namespaces`|:x:|
|`list_service_account_for_all_namespaces`|:x:|
|`list_service_for_all_namespaces`|:white_check_mark:|
|`patch_namespace`|:x:|
|`patch_namespace_status`|:x:|
|`patch_namespaced_config_map`|:x:|
|`patch_namespaced_endpoints`|:x:|
|`patch_namespaced_event`|:x:|
|`patch_namespaced_limit_range`|:x:|
|`patch_namespaced_persistent_volume_claim`|:x:|
|`patch_namespaced_persistent_volume_claim_status`|:x:|
|`patch_namespaced_pod`|:white_check_mark:|
|`patch_namespaced_pod_status`|:x:|
|`patch_namespaced_pod_template`|:x:|
|`patch_namespaced_replication_controller`|:x:|
|`patch_namespaced_replication_controller_scale`|:x:|
|`patch_namespaced_replication_controller_status`|:x:|
|`patch_namespaced_resource_quota`|:x:|
|`patch_namespaced_resource_quota_status`|:x:|
|`patch_namespaced_secret`|:x:|
|`patch_namespaced_service`|:white_check_mark:|
|`patch_namespaced_service_account`|:x:|
|`patch_namespaced_service_status`|:x:|
|`patch_node`|:x:|
|`patch_node_status`|:x:|
|`patch_persistent_volume`|:x:|
|`patch_persistent_volume_status`|:x:|
|`read_component_status`|:x:|
|`read_namespace`|:x:|
|`read_namespace_status`|:x:|
|`read_namespaced_config_map`|:x:|
|`read_namespaced_endpoints`|:x:|
|`read_namespaced_event`|:x:|
|`read_namespaced_limit_range`|:x:|
|`read_namespaced_persistent_volume_claim`|:x:|
|`read_namespaced_persistent_volume_claim_status`|:x:|
|`read_namespaced_pod`|:white_check_mark:|
|`read_namespaced_pod_log`|:white_check_mark:|
|`read_namespaced_pod_status`|:x:|
|`read_namespaced_pod_template`|:x:|
|`read_namespaced_replication_controller`|:x:|
|`read_namespaced_replication_controller_scale`|:x:|
|`read_namespaced_replication_controller_status`|:x:|
|`read_namespaced_resource_quota`|:x:|
|`read_namespaced_resource_quota_status`|:x:|
|`read_namespaced_secret`|:x:|
|`read_namespaced_service`|:x:|
|`read_namespaced_service_account`|:x:|
|`read_namespaced_service_status`|:x:|
|`read_node`|:x:|
|`read_node_status`|:x:|
|`read_persistent_volume`|:x:|
|`read_persistent_volume_status`|:x:|
|`replace_namespace`|:x:|
|`replace_namespace_finalize`|:x:|
|`replace_namespace_status`|:x:|
|`replace_namespaced_config_map`|:x:|
|`replace_namespaced_endpoints`|:x:|
|`replace_namespaced_event`|:x:|
|`replace_namespaced_limit_range`|:x:|
|`replace_namespaced_persistent_volume_claim`|:x:|
|`replace_namespaced_persistent_volume_claim_status`|:x:|
|`replace_namespaced_pod`|:white_check_mark:|
|`replace_namespaced_pod_status`|:x:|
|`replace_namespaced_pod_template`|:x:|
|`replace_namespaced_replication_controller`|:x:|
|`replace_namespaced_replication_controller_scale`|:x:|
|`replace_namespaced_replication_controller_status`|:x:|
|`replace_namespaced_resource_quota`|:x:|
|`replace_namespaced_resource_quota_status`|:x:|
|`replace_namespaced_secret`|:x:|
|`replace_namespaced_service`|:white_check_mark:|
|`replace_namespaced_service_account`|:x:|
|`replace_namespaced_service_status`|:x:|
|`replace_node`|:x:|
|`replace_node_status`|:x:|
|`replace_persistent_volume`|:x:|
|`replace_persistent_volume_status`|:x:|


### AppsV1Api
|method|supported?|
|---|---|
|`create_namespaced_controller_revision`|:x:|
|`create_namespaced_daemon_set`|:x:|
|`create_namespaced_deployment`|:x:|
|`create_namespaced_replica_set`|:x:|
|`create_namespaced_stateful_set`|:x:|
|`delete_collection_namespaced_controller_revision`|:x:|
|`delete_collection_namespaced_daemon_set`|:x:|
|`delete_collection_namespaced_deployment`|:x:|
|`delete_collection_namespaced_replica_set`|:x:|
|`delete_collection_namespaced_stateful_set`|:x:|
|`delete_namespaced_controller_revision`|:x:|
|`delete_namespaced_daemon_set`|:x:|
|`delete_namespaced_deployment`|:x:|
|`delete_namespaced_replica_set`|:x:|
|`delete_namespaced_stateful_set`|:x:|
|`get_api_resources`|:x:|
|`list_controller_revision_for_all_namespaces`|:x:|
|`list_daemon_set_for_all_namespaces`|:x:|
|`list_deployment_for_all_namespaces`|:x:|
|`list_namespaced_controller_revision`|:x:|
|`list_namespaced_daemon_set`|:x:|
|`list_namespaced_deployment`|:x:|
|`list_namespaced_replica_set`|:x:|
|`list_namespaced_stateful_set`|:x:|
|`list_replica_set_for_all_namespaces`|:x:|
|`list_stateful_set_for_all_namespaces`|:x:|
|`patch_namespaced_controller_revision`|:x:|
|`patch_namespaced_daemon_set`|:x:|
|`patch_namespaced_daemon_set_status`|:x:|
|`patch_namespaced_deployment`|:x:|
|`patch_namespaced_deployment_scale`|:x:|
|`patch_namespaced_deployment_status`|:x:|
|`patch_namespaced_replica_set`|:x:|
|`patch_namespaced_replica_set_scale`|:x:|
|`patch_namespaced_replica_set_status`|:x:|
|`patch_namespaced_stateful_set`|:x:|
|`patch_namespaced_stateful_set_scale`|:x:|
|`patch_namespaced_stateful_set_status`|:x:|
|`read_namespaced_controller_revision`|:x:|
|`read_namespaced_daemon_set`|:x:|
|`read_namespaced_daemon_set_status`|:x:|
|`read_namespaced_deployment`|:x:|
|`read_namespaced_deployment_scale`|:x:|
|`read_namespaced_deployment_status`|:x:|
|`read_namespaced_replica_set`|:x:|
|`read_namespaced_replica_set_scale`|:x:|
|`read_namespaced_replica_set_status`|:x:|
|`read_namespaced_stateful_set`|:x:|
|`read_namespaced_stateful_set_scale`|:x:|
|`read_namespaced_stateful_set_status`|:x:|
|`replace_namespaced_controller_revision`|:x:|
|`replace_namespaced_daemon_set`|:x:|
|`replace_namespaced_daemon_set_status`|:x:|
|`replace_namespaced_deployment`|:x:|
|`replace_namespaced_deployment_scale`|:x:|
|`replace_namespaced_deployment_status`|:x:|
|`replace_namespaced_replica_set`|:x:|
|`replace_namespaced_replica_set_scale`|:x:|
|`replace_namespaced_replica_set_status`|:x:|
|`replace_namespaced_stateful_set`|:x:|
|`replace_namespaced_stateful_set_scale`|:x:|
|`replace_namespaced_stateful_set_status`|:x:|

### NetworkingV1beta1Api
|method|supported?|
|---|---|
|`create_namespaced_ingress`|:x:|
|`delete_collection_namespaced_ingress`|:x:|
|`delete_namespaced_ingress`|:x:|
|`get_api_resources`|:x:|
|`list_ingress_for_all_namespaces`|:x:|
|`list_namespaced_ingress`|:x:|
|`patch_namespaced_ingress`|:x:|
|`patch_namespaced_ingress_status`|:x:|
|`read_namespaced_ingress`|:x:|
|`read_namespaced_ingress_status`|:x:|
|`replace_namespaced_ingress`|:x:|
|`replace_namespaced_ingress_status`|:x:|