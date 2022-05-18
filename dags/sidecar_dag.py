"""
Example usage of astrocloud locally using a local docker-desktop kubernetes cluster to run a csv writer
with a csv uploader sidecar
"""
from datetime import datetime

from airflow import DAG, configuration
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from kubernetes.client import models as k8s
import uuid

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2019, 1, 1),
}

with DAG(
    "sidecar_dag", schedule_interval=None, default_args=default_args
) as dag:
    # later this should be part of the variables for tasks
    DEBUG = False
    namespace = configuration.conf.get("kubernetes", "NAMESPACE")

    # This will detect the default namespace locally and read the
    # environment namespace when deployed to Astronomer.
    if namespace == "default":
        config_file = "/usr/local/airflow/include/.kube/config"
        in_cluster = False
    else:
        in_cluster = True
        config_file = None

    IMAGE_NAME = "sidecar-python"
    IMAGE_TAG = "latest"
    IMAGE = f"{IMAGE_NAME}:{IMAGE_TAG}"

    compute_resources = k8s.V1ResourceRequirements(
        limits={"cpu": "100m", "memory": "1Gi"},
        requests={"cpu": "100m", "memory": "1Gi"},
    )

    job_name = "test_sidecar_uploader"
    meta_name = f"{job_name}-{uuid.uuid4().hex}"
    metadata = k8s.V1ObjectMeta(name=(meta_name))
    full_pod_spec = k8s.V1Pod(
        metadata=metadata,
        spec=k8s.V1PodSpec(
            containers=[
                k8s.V1Container(
                    name="base",
                    resources=compute_resources,
                    image=IMAGE,
                    command=["python", "file_creator.py"],
                ),
                k8s.V1Container(
                    name="sidecar",
                    image=IMAGE,
                    command=["python", "sidecar_daemon.py"],
                ),
            ],
        ),
    )

    KubernetesPodOperator(
        namespace=namespace,
        name=job_name,
        task_id=job_name,
        in_cluster=in_cluster,  # if set to true, will look in the cluster, if false, looks for file
        cluster_context="docker-desktop",  # is ignored when in_cluster is set to True
        config_file=config_file,
        is_delete_operator_pod=False,
        get_logs=True,
        full_pod_spec=full_pod_spec,
        pod_template_file="/usr/local/airflow/pod_templates/sidecar_spec.yaml",
        startup_timeout_seconds=600,
    )
