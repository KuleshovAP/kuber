"""Собирает отчёт по пяти требованиям из исходников и журналов этой версии."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = {
    'app/requirements.txt': 'Обязательный список зависимостей внутри app: kafka-python и pytest. Именно этот путь используется Dockerfile и обоими вариантами CI.',
    'app/__init__.py': 'Объявляет Python-пакет app.',
    'app/kafka_client.py': 'Создаёт уникальный topic, отправляет UTF-8 JSON с acks=all, читает с earliest с тайм-аутом и сверяет событие. В finally закрывает клиентов и удаляет временный topic. Replication factor берётся из окружения: 1 в Compose, 3 в Kubernetes.',
    'app/main.py': 'Точка входа. По умолчанию выполняет один обмен; --continuous оставляет приложение работающим и повторяет обмен. Readiness-маркер появляется после успешного получения сообщения.',
    'Dockerfile': 'Корневой Dockerfile Python 3.11.11: копирует app/requirements.txt, устанавливает зависимости именно из него, затем копирует app и tests. Запускает python -m app.main.',
    'docker-compose.yml': 'Kafka 7.9.0 и ZooKeeper 7.9.0, постоянные тома, внутренний/внешний listeners и healthcheck Kafka. app запускается после готовности брокера. Provenance отключён для совместимости локального импорта образа.',
    'tests/unit/test_kafka_client.py': 'Проверяет сохранение Unicode и чисел при сериализации без брокера.',
    'tests/integration/test_integration.py': 'Проверяет настоящий обмен с Kafka, текст, значение, partition и offset уникального topic.',
    '.gitlab-ci.yml': 'GitLab pipeline со стадиями test/build/deploy: unit и integration, сборка/push по commit SHA, ручной deploy через deploy_script.sh.',
    '.github/workflows/ci.yml': 'Рабочая конфигурация GitHub Actions для push/PR/manual: unit и integration с реальной Kafka, сборка Docker-образа и сохранение диагностики.',
    'kafka-demo-deployment.yaml': 'Обязательный корневой манифест приложения: apps/v1 Deployment kafka-demo, одна реплика, постоянный процесс --continuous, readinessProbe после обмена с Kafka и ограничения ресурсов. Это не Job.',
    'k8s/namespace.yaml': 'Отдельный namespace kafka-homework в выбранном контексте docker-desktop.',
    'k8s/zookeeper.yaml': 'Headless Service и StatefulSet одиночного ZooKeeper с PVC 1 Gi и проверкой доступности TCP.',
    'k8s/kafka.yaml': 'Bootstrap Service, headless Service и StatefulSet трёх брокеров с PVC по 2 Gi. broker.id — числовой ordinal, advertised listener — DNS своего Pod. enableServiceLinks=false устраняет конфликт KAFKA_PORT.',
    'deploy_script.sh': 'Применяет StatefulSet-инфраструктуру и Deployment приложения, подставляет тег образа и ждёт готовности deployment/kafka-demo. Контекст задаётся явно.',
    'run_checks.ps1': 'Локальный сценарий: проверка Compose, запуск брокера, сборка, unit/integration, приложение и сохранение логов с проверкой exit code.',
    '.dockerignore': 'Исключает инструменты, журналы, архивы и кэши из Docker build context.',
    '.gitignore': 'Не позволяет публиковать инструменты, tar-архивы, кэши, виртуальные окружения, .env и kubeconfig.',
    'README.md': 'Инструкция, соответствующая обязательной структуре app/requirements.txt и запуску Deployment именно в Docker Desktop Kubernetes.',
    'build_report.py': 'Генерирует этот самодостаточный Markdown с полным исходным кодом, ссылкой на публикацию при её наличии и реальными журналами текущей версии.',
    'repository.json': 'Адрес предоставленного пользователем репозитория и проверенный статус публикации. published=true выставляется только после успешного push и проверки удалённого commit.',
}


def main():
    result = ['# Kafka, CI/CD и Kubernetes — исправленная версия\n\n',
              'Автор: Кулешов Алексей Петрович.\n\n',
              '## Исправления по замечаниям\n\n',
              '1. Зависимости находятся в **app/requirements.txt**, корневого requirements.txt в этой поставке нет. Dockerfile и CI обновлены.\n',
              '2. Подготовлены CI-файлы для GitHub и GitLab. Наличие настоящего репозитория подтверждается только ссылкой и commit ниже.\n',
              '3. Добавлен **kafka-demo-deployment.yaml** с **kind: Deployment**. Приложение имеет постоянный режим и readiness после реального обмена.\n',
              '4. Требуемая среда — Kubernetes, включённый в интерфейсе **Docker Desktop**, контекст **docker-desktop**. Прежний отдельный kind-кластер не считается подтверждением этого пункта.\n\n']
    publication = ROOT / 'repository.json'
    data = json.loads(publication.read_text(encoding='utf-8')) if publication.exists() else {}
    if data.get('published') and data.get('commit'):
        result += [f'## Репозиторий\n\n[Проект]({data["url"]})\n\nCommit: `{data["commit"]}`.\n\n']
    else:
        result += ['## Публикация: обязательный пункт ещё не завершён\n\n',
                   f'Целевой репозиторий: {data.get("url", "не указан")}. Для push ожидается авторизация с правом записи. ZIP или локальный Git не выдаются за выполненную публикацию. До публикации комплект не следует считать полностью готовым к пересдаче.\n\n']
    result += ['## Подтверждение запуска\n\n',
               'Только журналы **этой версии** ниже подтверждают выполненные проверки. Включение настройки без Ready Deployment не считается успешным запуском приложения.\n\n']
    for path in sorted((ROOT / 'evidence').glob('*')):
        raw = path.read_bytes()
        encoding = 'utf-16' if raw.startswith(b'\xff\xfe') else 'utf-8-sig'
        text = raw.decode(encoding, errors='replace')
        if len(text) > 12000:
            lines = text.splitlines()
            text = '\n'.join(lines[:12] + ['... середина журнала опущена; полный файл приложен ...'] + lines[-55:])
        result += [f'### evidence/{path.name}\n\n````text\n{text}\n````\n\n']
    result += ['## Назначение и полное содержимое файлов\n\n']
    for relative, description in FILES.items():
        path = ROOT / relative
        text = path.read_text(encoding='utf-8')
        result += [f'### {relative}\n\n{description}\n\n````text\n{text}\n````\n\n']
    result += ['## Источник по Docker Desktop Kubernetes\n\n',
               '[Официальная документация Docker](https://docs.docker.com/desktop/use-desktop/kubernetes/) описывает оба встроенных provisioner (kubeadm/kind) и контекст docker-desktop. Управляемый кластер Docker Desktop отличается от отдельного kind create cluster.\n']
    (ROOT / 'SOLUTION.md').write_text(''.join(result), encoding='utf-8')
    print('Created corrected SOLUTION.md')


if __name__ == '__main__':
    main()
