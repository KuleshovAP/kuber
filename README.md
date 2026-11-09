# Kafka: исправленное решение по пяти пунктам задания

## Структура

```text
homework_kafka_fixed/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── kafka_client.py
│   └── requirements.txt
├── tests/unit/test_kafka_client.py
├── tests/integration/test_integration.py
├── Dockerfile
├── docker-compose.yml
├── .gitlab-ci.yml
├── .github/workflows/ci.yml
├── kafka-demo-deployment.yaml
├── k8s/namespace.yaml
├── k8s/zookeeper.yaml
├── k8s/kafka.yaml
├── deploy_script.sh
├── run_checks.ps1
├── .dockerignore
├── .gitignore
├── README.md
├── build_report.py
├── SOLUTION.md
└── evidence/
```

**Список зависимостей расположен именно в `app/requirements.txt`.** В корне
исправленного проекта второго requirements.txt нет. Dockerfile и CI используют
`pip install -r app/requirements.txt`.

## 1. Kafka и ZooKeeper через Docker Compose

Нужны Windows x64 и запущенный Docker Desktop в режиме Linux containers.
Добавьте Docker CLI и kubectl в PATH, если команды не найдены:

```powershell
$env:PATH = "$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin;" + $env:PATH
docker compose up -d --wait kafka
docker compose ps
```

Kafka доступна с хоста по `localhost:9092`, из контейнеров — по `kafka:29092`.
ZooKeeper использует порт 2181 внутри сети Compose. Данные сохраняются в
named volumes. Healthcheck проверяет реальный запрос списка topic.

## 2–3. Приложение, образ, сообщение и тесты

```powershell
docker compose build app
docker compose run --rm app
docker compose run --rm app python -m pytest tests/unit tests/integration -v
```

Приложение создаёт уникальный topic, отправляет JSON, получает его обратно,
проверяет совпадение и печатает topic/partition/offset/received. Тестовый topic
удаляется после проверки. Ожидания ограничены тайм-аутами; старое сообщение
не может привести к ложному успеху. Producer использует `acks=all`.

Однократный запуск — режим по умолчанию для Compose. Для Kubernetes Deployment
предусмотрен `--continuous`: обмен повторяется каждые 30 секунд. После первого
успешного обмена создаётся `/tmp/kafka-demo-ready`; readinessProbe проверяет
этот файл. Приложение остаётся работающим, а не завершается как Job.

## 4. Публикация всего проекта и CI/CD

Проект должен находиться в настоящем репозитории GitHub либо GitLab.
Локальный ZIP, подготовленный YAML или локальный `git init` не заменяют
публикацию. Факт публикации подтверждается действительной ссылкой и commit SHA
в итоговом SOLUTION.md; если их нет, этот пункт ещё не завершён.

В GitHub используется `.github/workflows/ci.yml`: unit, сборка приложения,
запуск реальной Kafka, integration-тест и сохранение лога. В GitLab используется
`.gitlab-ci.yml`: test → build → manual deploy. Для Docker-in-Docker необходим
изолированный privileged runner. Учётные данные registry берутся из переменных
GitLab, пароль передаётся через stdin. Удалённое выполнение pipeline не
подменяется заявлением о локальных тестах.

`deploy_script.sh` применяет инфраструктуру Kafka и **Deployment приложения**,
подставляет переданный тег образа, ждёт rollout и выводит логи. Для него нужны
явный `KUBE_CONTEXT`, kubeconfig и доступ к указанному образу. Hosted runner
сам по себе не получает доступ к локальному Docker Desktop пользователя.

## 5. Kubernetes именно в Docker Desktop

Откройте **Docker Desktop → Kubernetes → Create cluster → Create**. Дождитесь
готовности кластера. В современных версиях Desktop доступны два встроенных
provisioner: kubeadm и kind. Оба относятся к Kubernetes **самого Docker Desktop**;
это описано в [официальной документации](https://docs.docker.com/desktop/use-desktop/kubernetes/).
Отдельная команда `kind create cluster` в этом решении не применяется.

Проверьте именно контекст `docker-desktop`:

```powershell
docker desktop kubernetes status
kubectl --context docker-desktop cluster-info
kubectl --context docker-desktop get nodes
```

Подготовьте образ с фиксированным тегом и примените манифесты:

```powershell
docker tag kafka-homework-app:local kafka-homework-app:desktop
kubectl --context docker-desktop apply -f k8s/namespace.yaml
kubectl --context docker-desktop apply -f k8s/zookeeper.yaml -f k8s/kafka.yaml
kubectl --context docker-desktop -n kafka-homework rollout status statefulset/zookeeper --timeout=300s
kubectl --context docker-desktop -n kafka-homework rollout status statefulset/kafka --timeout=600s
kubectl --context docker-desktop apply -f kafka-demo-deployment.yaml
kubectl --context docker-desktop -n kafka-homework rollout status deployment/kafka-demo --timeout=180s
kubectl --context docker-desktop -n kafka-homework get deployments,pods,pvc
kubectl --context docker-desktop -n kafka-homework logs deployment/kafka-demo --tail=10
```

`kafka-demo-deployment.yaml` находится в корне и содержит `kind: Deployment`,
одну реплику и постоянный процесс приложения. Kafka и ZooKeeper используют
StatefulSet и PVC: это инфраструктура, а не замена Deployment приложения.
Три брокера находятся на одном узле, поэтому пример не защищён от отказа узла.
ZooKeeper также одиночный. PLAINTEXT предназначен для учебной локальной сети.

Чтобы освободить память перед Kubernetes, можно остановить только учебные
Compose-сервисы: `docker compose stop kafka zookeeper`. Удалять тома не нужно.

Результаты текущей проверки приведены в SOLUTION.md и evidence. Прежние логи
контекста `kind-kafka-homework` не используются как доказательство работы
Docker Desktop Kubernetes.
