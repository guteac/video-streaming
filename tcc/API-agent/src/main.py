from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from kubernetes import client, config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para receber o ID do vídeo
class VideoRequest(BaseModel):
    videoId: str

class SpinnerDuration(BaseModel):
    videoId: str
    duration: str

KUBECONFIG="/usr/config"

config.load_kube_config(config_file=KUBECONFIG)

# Namespace onde os pods serão criados
K8S_NAMESPACE = "default"

# Nome da imagem do pod de transcodificação
FFMPEG_IMAGE = "guteactestdocker/ffmpeg-server:v1"

# Caminhos do PV no pod
VIDEO_INPUT_PATH = "/data/videos"

# Endpoint para iniciar o pod do FFmpeg
@app.post("/start", status_code=status.HTTP_201_CREATED)
async def start_video_stream(request: VideoRequest):
    video_id = request.videoId

    job_name = f"{video_id}-transcoder"

    # Configura o cliente da API do Kubernetes
    batch_v1 = client.BatchV1Api()

    # Verifica se o job já existe
    existing_jobs = batch_v1.list_namespaced_job(namespace=K8S_NAMESPACE, label_selector=f"app={job_name}")
    if existing_jobs.items:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Transcodificação em andamento")

    # Define o comando do FFmpeg
    ffmpeg_command = [
        "ffmpeg",
        "-re",
        "-i", f"{VIDEO_INPUT_PATH}/{video_id}.mp4",  # Arquivo de entrada
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-b:v", "2500k",
        "-c:a", "aac",
        "-b:a", "128k",
        "-f", "flv",
        f"rtmp://svc-video-server-rtmp/stream/{video_id}",  # Destino RTMP
    ]

    # Define o job para transcodificação
    job = client.V1Job(
        metadata=client.V1ObjectMeta(
            name=job_name,
            labels={"app": job_name},
        ),
        spec=client.V1JobSpec(
            backoff_limit=0,  # Não tenta recriar o pod em caso de falha
            ttl_seconds_after_finished=0, # Deleta a job após a execução
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": job_name}),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="ffmpeg",
                            image=FFMPEG_IMAGE,
                            command=ffmpeg_command,
                            volume_mounts=[
                                client.V1VolumeMount(
                                    name="videos",
                                    mount_path=VIDEO_INPUT_PATH,
                                ),
                            ],
                        )
                    ],
                    restart_policy="Never",
                    volumes=[
                        client.V1Volume(
                            name="videos",
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="pvc-ffmpeg-videos",
                            ),
                        ),
                    ],
                ),
            ),
        ),
    )

    # Cria o job no Kubernetes
    batch_v1.create_namespaced_job(namespace=K8S_NAMESPACE, body=job)

    return {"message": f"Transcodificação do vídeo {video_id} iniciada no job {job_name}."}

@app.post("/check", status_code=status.HTTP_200_OK)
async def check_video_stream(request: VideoRequest):
    video_id = request.videoId

    job_name = f"{video_id}-transcoder"

    batch_v1 = client.BatchV1Api()

    existing_jobs = batch_v1.list_namespaced_job(namespace=K8S_NAMESPACE, label_selector=f"app={job_name}")
    
    if existing_jobs.items:
        return {"message": f"Streamig do vídeo {video_id} em andamento."}
    else:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail='Container nao existe')

@app.post("/spinner-duration", status_code=status.HTTP_200_OK)
async def get_spinner_duration(request: SpinnerDuration):

    video_id = request.videoId
    duration = request.duration

    filename = "/tmp/"+video_id+".txt"

    with open(filename, 'a') as f:
        f.write(duration+"\n")

    return {"message": f"Duração do spinner capturada."}