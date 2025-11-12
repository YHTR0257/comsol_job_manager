# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, name)
);
```

### jobs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, COMSOL, VASP 等）の管理単位。

```sql
CREATE TABLE app.jobs (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES app.projects(id) ON DELETE CASCADE,
    created_by BIGINT REFERENCES app.users(id),
    name TEXT,
    description TEXT,
    type TEXT NOT NULL, -- 例: 'comsol', 'vasp'
cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, name)
);
```

### jobs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, COMSOL, VASP 等）の管理単位。

```sql
CREATE TABLE app.jobs (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES app.projects(id) ON DELETE CASCADE,
    created_by BIGINT REFERENCES app.users(id),
    name TEXT,
    description TEXT,
    type TEXT NOT NULL, -- 例: 'comsol', 'vasp'

    status TEXT NOT NULL DEFAULT 'pending', -- enum 風に扱う
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### job_runs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, name)
);
```

### jobs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, COMSOL, VASP 等）の管理単位。

```sql
CREATE TABLE app.jobs (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES app.projects(id) ON DELETE CASCADE,
    created_by BIGINT REFERENCES app.users(id),
    name TEXT,
    description TEXT,
    type TEXT NOT NULL, -- 例: 'comsol', 'vasp'
cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, name)
);
```

### jobs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, COMSOL, VASP 等）の管理単位。

```sql
CREATE TABLE app.jobs (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES app.projects(id) ON DELETE CASCADE,
    created_by BIGINT REFERENCES app.users(id),
    name TEXT,
    description TEXT,
    type TEXT NOT NULL, -- 例: 'comsol', 'vasp'

    status TEXT NOT NULL DEFAULT 'pending', -- enum 風に扱う
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### Job_runs



```sql
CREATE TABLE app.job_runs (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL REFERENCES app.jobs(id) ON DELETE CASCADE,
    run_number INT NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'queued', -- queued, running, success, failed
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    exit_code INT,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ON app.job_runs (job_id);
CREATE INDEX ON app.job_runs (status);
```

### files

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, name)
);
```

### jobs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, COMSOL, VASP 等）の管理単位。

```sql
CREATE TABLE app.jobs (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES app.projects(id) ON DELETE CASCADE,
    created_by BIGINT REFERENCES app.users(id),
    name TEXT,
    description TEXT,
    type TEXT NOT NULL, -- 例: 'comsol', 'vasp'
cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, name)
);
```

### jobs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, COMSOL, VASP 等）の管理単位。

```sql
CREATE TABLE app.jobs (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES app.projects(id) ON DELETE CASCADE,
    created_by BIGINT REFERENCES app.users(id),
    name TEXT,
    description TEXT,
    type TEXT NOT NULL, -- 例: 'comsol', 'vasp'

    status TEXT NOT NULL DEFAULT 'pending', -- enum 風に扱う
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### job_runs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, name)
);
```

### jobs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, COMSOL, VASP 等）の管理単位。

```sql
CREATE TABLE app.jobs (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES app.projects(id) ON DELETE CASCADE,
    created_by BIGINT REFERENCES app.users(id),
    name TEXT,
    description TEXT,
    type TEXT NOT NULL, -- 例: 'comsol', 'vasp'
cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, name)
);
```

### jobs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, COMSOL, VASP 等）の管理単位。

```sql
CREATE TABLE app.jobs (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES app.projects(id) ON DELETE CASCADE,
    created_by BIGINT REFERENCES app.users(id),
    name TEXT,
    description TEXT,
    type TEXT NOT NULL, -- 例: 'comsol', 'vasp'

    status TEXT NOT NULL DEFAULT 'pending', -- enum 風に扱う
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### Job_runs



```sql
CREATE TABLE app.job_runs (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL REFERENCES app.jobs(id) ON DELETE CASCADE,
    run_number INT NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'queued', -- queued, running, success, failed
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    exit_code INT,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ON app.job_runs (job_id);
CREATE INDEX ON app.job_runs (status);\! . 2to3 2to3-3.11 \: \[ \[\[ ]] __nvcc_device_query __updateEnvCache __updateEnvCacheAA __vsc_command_complete __vsc_command_output_start __vsc_continuation_end __vsc_continuation_start __vsc_escape_value __vsc_escape_value_fast __vsc_get_trap __vsc_precmd __vsc_preexec __vsc_preexec_only __vsc_prompt_cmd __vsc_prompt_cmd_original __vsc_prompt_end __vsc_prompt_start __vsc_report_prompt __vsc_restore_exit_code __vsc_update_cwd __vsc_update_env __vsc_update_prompt activate add-shell addgnupghome addgroup addpart addr2line adduser adig agetty ahost alembic alert alias applygnupgdefaults apt apt-cache apt-cdrom apt-config apt-get apt-key apt-mark ar arch archspec as awk b2sum backend-test-tools badblocks base32 base64 basename basenc bash bashbug bg bin2c bind blkdiscard blkid blkzone blockdev break bsdcat bsdcpio bsdtar bsdunzip builtin bunzip2 bzcat bzcmp bzdiff bzegrep bzexe bzfgrep bzgrep bzip2 bzip2recover bzless bzmore c++ c++filt c89 c89-gcc c99 c99-gcc c_rehash caller captoinfo case cat cc ccmake cd chage chardetect chattr chcon chcpu check-model check-node chfn chgpasswd chgrp chmem chmod choom chown chpasswd chroot chrt chsh cksum claude clear clear_console cmake cmp code comm command compgen compile_et complete compopt compute-sanitizer conda conda-build conda-convert conda-debug conda-develop conda-env conda-inspect conda-metapackage conda-render conda-skeleton conda2solv continue copilot-debug coproc corelist corepack cp cpack cpan cpan5.34-x86_64-linux-gnu cpgr cph cpp cpp-11 cppw csplit ctest ctrlaltdel cu++filt cuda-gdb cuda-gdbserver cuda-memcheck cudafe++ cuobjdump curl curl-config cut cvtsudoers dash date dd deactivate deb-systemd-helper deb-systemd-invoke debconf debconf-apt-progress debconf-communicate debconf-copydb debconf-escape debconf-set-selections debconf-show debugfs debugpy debugpy-adapter declare delgroup delpart deluser derb df diff diff3 dir dircolors dirmngr dirmngr-client dirname dirs disown distro dmesg dnsdomainname do domainname done dotenv dpkg dpkg-architecture dpkg-buildflags dpkg-buildpackage dpkg-checkbuilddeps dpkg-deb dpkg-distaddfile dpkg-divert dpkg-genbuildinfo dpkg-genchanges dpkg-gencontrol dpkg-gensymbols dpkg-maintscript-helper dpkg-mergechangelogs dpkg-name dpkg-parsechangelog dpkg-preconfigure dpkg-query dpkg-realpath dpkg-reconfigure dpkg-scanpackages dpkg-scansources dpkg-shlibdeps dpkg-source dpkg-split dpkg-statoverride dpkg-trigger dpkg-vendor du dumpe2fs dumpsolv dwp e2freefrag e2fsck e2image e2label e2mmpstatus e2scrub e2scrub_all e2undo e4crypt e4defrag echo ed2k-link editor edonr256-hash edonr512-hash egrep elfedit elif else enable enc2xs encguess env esac eval ex exec exit expand expiry export expr f2py factor faillock faillog fallocate false fatbinary fc feff_plot_cross_section feff_plot_dos fg fgrep fi filefrag fincore find findfs findmnt flock fmt fold fonttools for free fsck fsck.cramfs fsck.ext2 fsck.ext3 fsck.ext4 fsck.minix fsfreeze fstab-decode fstrim function g++ g++-11 gcc gcc-11 gcc-ar gcc-ar-11 gcc-nm gcc-nm-11 gcc-ranlib gcc-ranlib-11 gcov gcov-11 gcov-dump gcov-dump-11 gcov-tool gcov-tool-11 gemini genbrk gencat gencfu gencnval gendict genrb get_environment getconf getent getopt getopts getty git git-receive-pack git-shell git-upload-archive git-upload-pack gmake gold gost12-256-hash gost12-512-hash gpasswd gpg gpg-agent gpg-connect-agent gpg-wks-server gpg-zip gpg2 gpgcompose gpgconf gpgparsemail gpgsm gpgsplit gpgtar gpgv gprof grep groupadd groupdel groupmems groupmod groups grpck grpconv grpunconv gss-client gunzip gzexe gzip h2ph h2xs hardlink has160-hash hash head help helpztags history hostid hostname httpx hwclock hypothesis i386 iconv iconvconfig icu-config icuexportdata icuinfo id idle3 idle3.11 if in infocmp infotocap initctl install installcheck installkernel instmodsh invoke-rc.d ionice ipcmk ipcrm ipcs ipython ipython3 ischroot isosize isympy jlpm jobs join json_pp jsondiff jsonpatch jsonpointer jsonschema jupyter jupyter-dejavu jupyter-events jupyter-execute jupyter-kernel jupyter-kernelspec jupyter-lab jupyter-labextension jupyter-labhub jupyter-migrate jupyter-nbconvert jupyter-run jupyter-server jupyter-troubleshoot jupyter-trust k5srvutil kadmin kbxutil kdestroy keyctl kill killall5 kinit klist kpasswd krb5-config kswitch ktutil kvno l la last lastb lastlog ld ld.bfd ld.gold ldattach ldconfig ldconfig.real ldd let libnetcfg libpng-config libpng16-config link lintrunner linux32 linux64 ll ln local locale locale-check localedef logger login logname logout logsave losetup ls lsattr lsblk lscpu lsipc lslocks lslogins lsmem lsns lspgpot lto-dump-11 lz4 lz4c lz4cat lzcat lzcmp lzdiff lzegrep lzfgrep lzgrep lzless lzma lzmainfo lzmore magnet-link make make-first-existing-target makeconv mako-render mamba mamba-package man mapfile markdown_py mawk mcookie md5sum md5sum.textutils mergesolv mesg migrate-pubring-from-classic-gpg mkdir mke2fs mkfifo mkfs mkfs.bfs mkfs.cramfs mkfs.ext2 mkfs.ext3 mkfs.ext4 mkfs.minix mkhomedir_helper mklost+found mknod mkswap mktemp more mount mountpoint mv namei nawk ncu ncu-ui ncurses6-config ncursesw6-config newgrp newusers nghttp nghttpd nghttpx nice ninja nisdomainname nl nm node nodejs nohup nologin normalizer npm nproc npx nsenter numfmt nv-nsight-cu nv-nsight-cu-cli nvcc nvdisasm nvlink nvprof nvprune objcopy objdump od openssl optuna pager pam-auth-update pam_extrausers_chkpwd pam_extrausers_update pam_getenv pam_timestamp_check partx passwd paste patch patchelf pathchk pdb3 pdb3.10 perl perl5.34-x86_64-linux-gnu perl5.34.0 perlbug perldoc perlivp perlthanks pgrep piconv pidof pidwait pinentry pinentry-curses pinky pip pip3 pip3.11 pivot_root pkgdata pkginfo pkill pl2pm pldd plotly_get_chrome pmap pmg pod2html pod2man pod2text pod2usage podchecker policy-rc.d popd pr printenv printf prlimit proton proton-viewer prove ps ptar ptardiff ptargrep ptx ptxas pushd pwck pwconv pwd pwdx pwunconv py.test py3clean py3compile py3versions pybabel pydoc pydoc3 pydoc3.10 pydoc3.11 pyftmerge pyftsubset pygettext3 pygettext3.10 pygmentize pyjson5 pytest python python3 python3-config python3.1 python3.10 python3.11 python3.11-config ranlib rbash rcp read readarray readelf readlink readonly readprofile realpath remove-shell renice repo2solv reset resize2fs resizepart return rev rg rgrep rhash rlogin rm rmdir rmt rmt-tar rpcgen rrsync rsh rsync rsync-ssl rtcwake run-parts runcon runuser rview rvim savelog sclient scp script scriptlive scriptreplay sdiff sed select select-editor send2trash sensible-browser sensible-editor sensible-pager seq service set setarch setpriv setsid setterm sftp sfv-hash sg sh sha1sum sha224sum sha256sum sha384sum sha512sum shadowconfig shasum shift shopt shred shuf sim_client size skill slabtop sleep slogin snice sort source splain split sqlite3_analyzer ssh ssh-add ssh-agent ssh-argv0 ssh-copy-id ssh-keygen ssh-keyscan start-stop-daemon stat stdbuf streamzip strings strip stty su sudo sudo_logsrvd sudo_sendlog sudoedit sudoreplay sulogin sum suspend swaplabel swapoff swapon switch_root sync sysctl sz_split sz_wc tabs tabulate tac tail tar tarcat taskset tclsh tclsh8.6 tee tempfile tensorboard test testsolv then tic tiger-hash time timeout times tload toe top torchfrtrace torchrun touch tput tqdm tr trap true truncate tset tsort tth-hash ttx tty tune2fs type typeset tzselect uclampset ulimit umask umount unalias uname uncompress unexpand uniq unix_chkpwd unix_update unlink unlz4 unlzma unminimize unset unshare until unxz unzstd update-alternatives update-ca-certificates update-passwd update-rc.d update-shells uptime useradd userdel usermod users utmpdump uuclient vdir vi view vigr vim vim.basic vimdiff vimtutor vipw visudo vmstat w wait wall wandb watch watchgnupg wb wc wdctl wget wheel whereis which which.debianutils while whirlpool-hash who whoami wipefs wish wish8.6 wsdump x86_64 x86_64-conda-linux-gnu-ld x86_64-conda_cos6-linux-gnu-ld x86_64-linux-gnu-addr2line x86_64-linux-gnu-ar x86_64-linux-gnu-as x86_64-linux-gnu-c++filt x86_64-linux-gnu-cpp x86_64-linux-gnu-cpp-11 x86_64-linux-gnu-dwp x86_64-linux-gnu-elfedit x86_64-linux-gnu-g++ x86_64-linux-gnu-g++-11 x86_64-linux-gnu-gcc x86_64-linux-gnu-gcc-11 x86_64-linux-gnu-gcc-ar x86_64-linux-gnu-gcc-ar-11 x86_64-linux-gnu-gcc-nm x86_64-linux-gnu-gcc-nm-11 x86_64-linux-gnu-gcc-ranlib x86_64-linux-gnu-gcc-ranlib-11 x86_64-linux-gnu-gcov x86_64-linux-gnu-gcov-11 x86_64-linux-gnu-gcov-dump x86_64-linux-gnu-gcov-dump-11 x86_64-linux-gnu-gcov-tool x86_64-linux-gnu-gcov-tool-11 x86_64-linux-gnu-gold x86_64-linux-gnu-gprof x86_64-linux-gnu-ld x86_64-linux-gnu-ld.bfd x86_64-linux-gnu-ld.gold x86_64-linux-gnu-lto-dump-11 x86_64-linux-gnu-nm x86_64-linux-gnu-objcopy x86_64-linux-gnu-objdump x86_64-linux-gnu-ranlib x86_64-linux-gnu-readelf x86_64-linux-gnu-size x86_64-linux-gnu-strings x86_64-linux-gnu-strip xargs xml2-config xmlcatalog xmllint xsubpp xxd xz xzcat xzcmp xzdiff xzegrep xzfgrep xzgrep xzless xzmore yes ypdomainname zcat zcmp zdiff zdump zegrep zfgrep zforce zgrep zic zipdetails zless zmore znew zramctl zstd zstdcat Zstdgrep 

```sql
CREATE TABLE app.files (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT REFERENCES app.projects(id) ON DELETE SET NULL,
    job_run_id BIGINT REFERENCES app.job_runs(id) ON DELETE SET NULL,
    name TEXT NOT NULL,
    mime_type TEXT,
    storage_path TEXT NOT NULL, -- S3キーやパス
    size_bytes BIGINT,
    created_by BIGINT REFERENCES app.users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ON app.files (project_id);
CREATE INDEX ON app.files (job_run_id);
```

### materials

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, name)
);
```

### jobs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, COMSOL, VASP 等）の管理単位。

```sql
CREATE TABLE app.jobs (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES app.projects(id) ON DELETE CASCADE,
    created_by BIGINT REFERENCES app.users(id),
    name TEXT,
    description TEXT,
    type TEXT NOT NULL, -- 例: 'comsol', 'vasp'
cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, name)
);
```

### jobs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, COMSOL, VASP 等）の管理単位。

```sql
CREATE TABLE app.jobs (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES app.projects(id) ON DELETE CASCADE,
    created_by BIGINT REFERENCES app.users(id),
    name TEXT,
    description TEXT,
    type TEXT NOT NULL, -- 例: 'comsol', 'vasp'

    status TEXT NOT NULL DEFAULT 'pending', -- enum 風に扱う
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### job_runs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, name)
);
```

### jobs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, COMSOL, VASP 等）の管理単位。

```sql
CREATE TABLE app.jobs (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES app.projects(id) ON DELETE CASCADE,
    created_by BIGINT REFERENCES app.users(id),
    name TEXT,
    description TEXT,
    type TEXT NOT NULL, -- 例: 'comsol', 'vasp'
cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, name)
);
```

### jobs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, COMSOL, VASP 等）の管理単位。

```sql
CREATE TABLE app.jobs (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES app.projects(id) ON DELETE CASCADE,
    created_by BIGINT REFERENCES app.users(id),
    name TEXT,
    description TEXT,
    type TEXT NOT NULL, -- 例: 'comsol', 'vasp'

    status TEXT NOT NULL DEFAULT 'pending', -- enum 風に扱う
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### Job_runs



```sql
CREATE TABLE app.job_runs (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL REFERENCES app.jobs(id) ON DELETE CASCADE,
    run_number INT NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'queued', -- queued, running, success, failed
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    exit_code INT,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ON app.job_runs (job_id);
CREATE INDEX ON app.job_runs (status);
```

### files

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, name)
);
```

### jobs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, COMSOL, VASP 等）の管理単位。

```sql
CREATE TABLE app.jobs (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES app.projects(id) ON DELETE CASCADE,
    created_by BIGINT REFERENCES app.users(id),
    name TEXT,
    description TEXT,
    type TEXT NOT NULL, -- 例: 'comsol', 'vasp'
cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, name)
);
```

### jobs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, COMSOL, VASP 等）の管理単位。

```sql
CREATE TABLE app.jobs (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES app.projects(id) ON DELETE CASCADE,
    created_by BIGINT REFERENCES app.users(id),
    name TEXT,
    description TEXT,
    type TEXT NOT NULL, -- 例: 'comsol', 'vasp'

    status TEXT NOT NULL DEFAULT 'pending', -- enum 風に扱う
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### job_runs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, name)
);
```

### jobs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, COMSOL, VASP 等）の管理単位。

```sql
CREATE TABLE app.jobs (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES app.projects(id) ON DELETE CASCADE,
    created_by BIGINT REFERENCES app.users(id),
    name TEXT,
    description TEXT,
    type TEXT NOT NULL, -- 例: 'comsol', 'vasp'
cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, name)
);
```

### jobs

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### projects

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

cat > /workspace/docs/database.md <<'EOF'
# Overview

>

:
'Eof'>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

> `public` のほかにアプリケーション専用スキーマを作成することを推奨します。

:

```sql
-- アプリケーション用スキーマ
CREATE SCHEMA IF NOT EXISTS app;

-- 分析用や履歴用スキーマを分ける場合
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;
```

 `app` スキーマ下に配置します。

---

## Core table definitions (サンプル)

'EOF'>

### users

cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



cat > /workspace/docs/database.md <<EOF
# Overview

>

:
Eof>VASP結果など）を SQL レベルで定義するサンプルを提供する。
- 運用上のインデックスや整合性制約、バックアップ/マイグレーションの注意点を提示する。

: 以下の定義はサンプルであり、実運用時はアプリケーションの要件（認証方式、権限モデル、パフォーマンス要件）に合わせて適宜調整してください。

---

## Schemas

>  のほかにアプリケーション専用スキーマを作成することを推奨します。

:



  スキーマ下に配置します。

---

## Core table definitions (サンプル)

EOF>

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests tmp Users

.devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests Tmp (OAuth, LDAP など) を使う場合は最小限にします。 

```sql
CREATE TABLE app.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 履歴追跡やトリガーで updated_at を自動更新することを推奨
```

### Projects



```sql
CREATE TABLE app.projects (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_public BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, COMSOL, VASP 等）の管理単位。

```sql
CREATE TABLE app.jobs (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES app.projects(id) ON DELETE CASCADE,
    created_by BIGINT REFERENCES app.users(id),
    name TEXT,
    description TEXT,
    type TEXT NOT NULL, -- 例: 'comsol', 'vasp'

    status TEXT NOT NULL DEFAULT 'pending', -- enum 風に扱う
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### Job_runs



```sql
CREATE TABLE app.job_runs (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL REFERENCES app.jobs(id) ON DELETE CASCADE,
    run_number INT NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'queued', -- queued, running, success, failed
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    exit_code INT,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ON app.job_runs (job_id);
CREATE INDEX ON app.job_runs (status);\! . 2to3 2to3-3.11 \: \[ \[\[ ]] __nvcc_device_query __updateEnvCache __updateEnvCacheAA __vsc_command_complete __vsc_command_output_start __vsc_continuation_end __vsc_continuation_start __vsc_escape_value __vsc_escape_value_fast __vsc_get_trap __vsc_precmd __vsc_preexec __vsc_preexec_only __vsc_prompt_cmd __vsc_prompt_cmd_original __vsc_prompt_end __vsc_prompt_start __vsc_report_prompt __vsc_restore_exit_code __vsc_update_cwd __vsc_update_env __vsc_update_prompt activate add-shell addgnupghome addgroup addpart addr2line adduser adig agetty ahost alembic alert alias applygnupgdefaults apt apt-cache apt-cdrom apt-config apt-get apt-key apt-mark ar arch archspec as awk b2sum backend-test-tools badblocks base32 base64 basename basenc bash bashbug bg bin2c bind blkdiscard blkid blkzone blockdev break bsdcat bsdcpio bsdtar bsdunzip builtin bunzip2 bzcat bzcmp bzdiff bzegrep bzexe bzfgrep bzgrep bzip2 bzip2recover bzless bzmore c++ c++filt c89 c89-gcc c99 c99-gcc c_rehash caller captoinfo case cat cc ccmake cd chage chardetect chattr chcon chcpu check-model check-node chfn chgpasswd chgrp chmem chmod choom chown chpasswd chroot chrt chsh cksum claude clear clear_console cmake cmp code comm command compgen compile_et complete compopt compute-sanitizer conda conda-build conda-convert conda-debug conda-develop conda-env conda-inspect conda-metapackage conda-render conda-skeleton conda2solv continue copilot-debug coproc corelist corepack cp cpack cpan cpan5.34-x86_64-linux-gnu cpgr cph cpp cpp-11 cppw csplit ctest ctrlaltdel cu++filt cuda-gdb cuda-gdbserver cuda-memcheck cudafe++ cuobjdump curl curl-config cut cvtsudoers dash date dd deactivate deb-systemd-helper deb-systemd-invoke debconf debconf-apt-progress debconf-communicate debconf-copydb debconf-escape debconf-set-selections debconf-show debugfs debugpy debugpy-adapter declare delgroup delpart deluser derb df diff diff3 dir dircolors dirmngr dirmngr-client dirname dirs disown distro dmesg dnsdomainname do domainname done dotenv dpkg dpkg-architecture dpkg-buildflags dpkg-buildpackage dpkg-checkbuilddeps dpkg-deb dpkg-distaddfile dpkg-divert dpkg-genbuildinfo dpkg-genchanges dpkg-gencontrol dpkg-gensymbols dpkg-maintscript-helper dpkg-mergechangelogs dpkg-name dpkg-parsechangelog dpkg-preconfigure dpkg-query dpkg-realpath dpkg-reconfigure dpkg-scanpackages dpkg-scansources dpkg-shlibdeps dpkg-source dpkg-split dpkg-statoverride dpkg-trigger dpkg-vendor du dumpe2fs dumpsolv dwp e2freefrag e2fsck e2image e2label e2mmpstatus e2scrub e2scrub_all e2undo e4crypt e4defrag echo ed2k-link editor edonr256-hash edonr512-hash egrep elfedit elif else enable enc2xs encguess env esac eval ex exec exit expand expiry export expr f2py factor faillock faillog fallocate false fatbinary fc feff_plot_cross_section feff_plot_dos fg fgrep fi filefrag fincore find findfs findmnt flock fmt fold fonttools for free fsck fsck.cramfs fsck.ext2 fsck.ext3 fsck.ext4 fsck.minix fsfreeze fstab-decode fstrim function g++ g++-11 gcc gcc-11 gcc-ar gcc-ar-11 gcc-nm gcc-nm-11 gcc-ranlib gcc-ranlib-11 gcov gcov-11 gcov-dump gcov-dump-11 gcov-tool gcov-tool-11 gemini genbrk gencat gencfu gencnval gendict genrb get_environment getconf getent getopt getopts getty git git-receive-pack git-shell git-upload-archive git-upload-pack gmake gold gost12-256-hash gost12-512-hash gpasswd gpg gpg-agent gpg-connect-agent gpg-wks-server gpg-zip gpg2 gpgcompose gpgconf gpgparsemail gpgsm gpgsplit gpgtar gpgv gprof grep groupadd groupdel groupmems groupmod groups grpck grpconv grpunconv gss-client gunzip gzexe gzip h2ph h2xs hardlink has160-hash hash head help helpztags history hostid hostname httpx hwclock hypothesis i386 iconv iconvconfig icu-config icuexportdata icuinfo id idle3 idle3.11 if in infocmp infotocap initctl install installcheck installkernel instmodsh invoke-rc.d ionice ipcmk ipcrm ipcs ipython ipython3 ischroot isosize isympy jlpm jobs join json_pp jsondiff jsonpatch jsonpointer jsonschema jupyter jupyter-dejavu jupyter-events jupyter-execute jupyter-kernel jupyter-kernelspec jupyter-lab jupyter-labextension jupyter-labhub jupyter-migrate jupyter-nbconvert jupyter-run jupyter-server jupyter-troubleshoot jupyter-trust k5srvutil kadmin kbxutil kdestroy keyctl kill killall5 kinit klist kpasswd krb5-config kswitch ktutil kvno l la last lastb lastlog ld ld.bfd ld.gold ldattach ldconfig ldconfig.real ldd let libnetcfg libpng-config libpng16-config link lintrunner linux32 linux64 ll ln local locale locale-check localedef logger login logname logout logsave losetup ls lsattr lsblk lscpu lsipc lslocks lslogins lsmem lsns lspgpot lto-dump-11 lz4 lz4c lz4cat lzcat lzcmp lzdiff lzegrep lzfgrep lzgrep lzless lzma lzmainfo lzmore magnet-link make make-first-existing-target makeconv mako-render mamba mamba-package man mapfile markdown_py mawk mcookie md5sum md5sum.textutils mergesolv mesg migrate-pubring-from-classic-gpg mkdir mke2fs mkfifo mkfs mkfs.bfs mkfs.cramfs mkfs.ext2 mkfs.ext3 mkfs.ext4 mkfs.minix mkhomedir_helper mklost+found mknod mkswap mktemp more mount mountpoint mv namei nawk ncu ncu-ui ncurses6-config ncursesw6-config newgrp newusers nghttp nghttpd nghttpx nice ninja nisdomainname nl nm node nodejs nohup nologin normalizer npm nproc npx nsenter numfmt nv-nsight-cu nv-nsight-cu-cli nvcc nvdisasm nvlink nvprof nvprune objcopy objdump od openssl optuna pager pam-auth-update pam_extrausers_chkpwd pam_extrausers_update pam_getenv pam_timestamp_check partx passwd paste patch patchelf pathchk pdb3 pdb3.10 perl perl5.34-x86_64-linux-gnu perl5.34.0 perlbug perldoc perlivp perlthanks pgrep piconv pidof pidwait pinentry pinentry-curses pinky pip pip3 pip3.11 pivot_root pkgdata pkginfo pkill pl2pm pldd plotly_get_chrome pmap pmg pod2html pod2man pod2text pod2usage podchecker policy-rc.d popd pr printenv printf prlimit proton proton-viewer prove ps ptar ptardiff ptargrep ptx ptxas pushd pwck pwconv pwd pwdx pwunconv py.test py3clean py3compile py3versions pybabel pydoc pydoc3 pydoc3.10 pydoc3.11 pyftmerge pyftsubset pygettext3 pygettext3.10 pygmentize pyjson5 pytest python python3 python3-config python3.1 python3.10 python3.11 python3.11-config ranlib rbash rcp read readarray readelf readlink readonly readprofile realpath remove-shell renice repo2solv reset resize2fs resizepart return rev rg rgrep rhash rlogin rm rmdir rmt rmt-tar rpcgen rrsync rsh rsync rsync-ssl rtcwake run-parts runcon runuser rview rvim savelog sclient scp script scriptlive scriptreplay sdiff sed select select-editor send2trash sensible-browser sensible-editor sensible-pager seq service set setarch setpriv setsid setterm sftp sfv-hash sg sh sha1sum sha224sum sha256sum sha384sum sha512sum shadowconfig shasum shift shopt shred shuf sim_client size skill slabtop sleep slogin snice sort source splain split sqlite3_analyzer ssh ssh-add ssh-agent ssh-argv0 ssh-copy-id ssh-keygen ssh-keyscan start-stop-daemon stat stdbuf streamzip strings strip stty su sudo sudo_logsrvd sudo_sendlog sudoedit sudoreplay sulogin sum suspend swaplabel swapoff swapon switch_root sync sysctl sz_split sz_wc tabs tabulate tac tail tar tarcat taskset tclsh tclsh8.6 tee tempfile tensorboard test testsolv then tic tiger-hash time timeout times tload toe top torchfrtrace torchrun touch tput tqdm tr trap true truncate tset tsort tth-hash ttx tty tune2fs type typeset tzselect uclampset ulimit umask umount unalias uname uncompress unexpand uniq unix_chkpwd unix_update unlink unlz4 unlzma unminimize unset unshare until unxz unzstd update-alternatives update-ca-certificates update-passwd update-rc.d update-shells uptime useradd userdel usermod users utmpdump uuclient vdir vi view vigr vim vim.basic vimdiff vimtutor vipw visudo vmstat w wait wall wandb watch watchgnupg wb wc wdctl wget wheel whereis which which.debianutils while whirlpool-hash who whoami wipefs wish wish8.6 wsdump x86_64 x86_64-conda-linux-gnu-ld x86_64-conda_cos6-linux-gnu-ld x86_64-linux-gnu-addr2line x86_64-linux-gnu-ar x86_64-linux-gnu-as x86_64-linux-gnu-c++filt x86_64-linux-gnu-cpp x86_64-linux-gnu-cpp-11 x86_64-linux-gnu-dwp x86_64-linux-gnu-elfedit x86_64-linux-gnu-g++ x86_64-linux-gnu-g++-11 x86_64-linux-gnu-gcc x86_64-linux-gnu-gcc-11 x86_64-linux-gnu-gcc-ar x86_64-linux-gnu-gcc-ar-11 x86_64-linux-gnu-gcc-nm x86_64-linux-gnu-gcc-nm-11 x86_64-linux-gnu-gcc-ranlib x86_64-linux-gnu-gcc-ranlib-11 x86_64-linux-gnu-gcov x86_64-linux-gnu-gcov-11 x86_64-linux-gnu-gcov-dump x86_64-linux-gnu-gcov-dump-11 x86_64-linux-gnu-gcov-tool x86_64-linux-gnu-gcov-tool-11 x86_64-linux-gnu-gold x86_64-linux-gnu-gprof x86_64-linux-gnu-ld x86_64-linux-gnu-ld.bfd x86_64-linux-gnu-ld.gold x86_64-linux-gnu-lto-dump-11 x86_64-linux-gnu-nm x86_64-linux-gnu-objcopy x86_64-linux-gnu-objdump x86_64-linux-gnu-ranlib x86_64-linux-gnu-readelf x86_64-linux-gnu-size x86_64-linux-gnu-strings x86_64-linux-gnu-strip xargs xml2-config xmlcatalog xmllint xsubpp xxd xz xzcat xzcmp xzdiff xzegrep xzfgrep xzgrep xzless xzmore yes ypdomainname zcat zcmp zdiff zdump zegrep zfgrep zforce zgrep zic zipdetails zless zmore znew zramctl zstd zstdcat Zstdgrep 

```sql
CREATE TABLE app.files (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT REFERENCES app.projects(id) ON DELETE SET NULL,
    job_run_id BIGINT REFERENCES app.job_runs(id) ON DELETE SET NULL,
    name TEXT NOT NULL,
    mime_type TEXT,
    storage_path TEXT NOT NULL, -- S3キーやパス
    size_bytes BIGINT,
    created_by BIGINT REFERENCES app.users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ON app.files (project_id);
CREATE INDEX ON app.files (job_run_id);
```

### .devcontainer .env .git .gitignore .vscode README.md data docker docker-compose.dev.yml docker-compose.prod.yml docs logs src templates tests `src/data/models` に material 関連のクラスがあるため、連携用に想定。Tmp 

```sql
CREATE TABLE app.materials (
    id BIGSERIAL PRIMARY KEY,
    external_id TEXT UNIQUE, -- 外部システム識別子
    name TEXT,
    composition JSONB,
    properties JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### vasp_results

VASP などの計算結果を格納する軽量なメタテーブル。詳細はパーケットやオブジェクトストレージで管理する。

```sql
CREATE TABLE app.vasp_results (
    id BIGSERIAL PRIMARY KEY,
    job_run_id BIGINT REFERENCES app.job_runs(id) ON DELETE CASCADE,
    result_path TEXT, -- parquet / s3 path
    summary JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ON app.vasp_results (job_run_id);
```

### audit.logs (履歴)

> `audit` スキーマを使います。

```sql
CREATE TABLE audit.logs (
    id BIGSERIAL PRIMARY KEY,
    who BIGINT REFERENCES app.users(id),
    action TEXT NOT NULL,
    object_type TEXT,
    object_id TEXT,
    payload JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ON audit.logs (who);
CREATE INDEX ON audit.logs (action);
```

---

## インデックスとパフォーマンス

- 検索が多いカラム（status, job_id, project_id, created_at 等）には適切にインデックスを張る。
- JSONB カラムに対しては用途に応じて GIN インデックスを使う。例:

```sql
CREATE INDEX ON app.jobs USING GIN (parameters);
CREATE INDEX ON app.materials USING GIN (properties);
```

- レンジクエリ（日時範囲）を多用する場合は、必要に応じてパーティショニング（例: job_runs を created_at で月次パーティション）を検討する。

---

## 外部キーと削除ポリシー

- ユースケースに応じて ON DELETE の挙動を選ぶ（CASCADE / SET NULL / RESTRICT）。
- 重要なビジネスデータは安易に CASCADE しない方がよい（誤削除リスク）。

---

## マイグレーションと運用ノート

- スキーマ変更は Flyway, Alembic, Django Migrations などのツールで管理することを推奨。
- 重大な ALTER（列の型変更、大きなデータ移動）はオフラインメンテナンスや段階的ロールアウトを計画する。
- 大規模テーブルにインデックスを追加する際は CONCURRENTLY を使う:

```sql
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_job_runs_status ON app.job_runs (status);
```

- バックアップ: 定期的な basebackup + WAL アーカイブを推奨。重要テーブルは論理バックアップ（pg_dump）も併用する。

---

## ER（概念図の説明）

- `users` 1 - N `projects`
- `projects` 1 - N `jobs`
- `jobs` 1 - N `job_runs`
- `job_runs` 1 - N `files`, 1 - N `vasp_results`

---

## 例: よく使うクエリ

:

```sql
SELECT jr.*
FROM app.job_runs jr
JOIN app.jobs j ON j.id = jr.job_id
WHERE jr.status = 'failed'
  AND jr.finished_at > now() - interval '7 days'
ORDER BY jr.finished_at DESC;
```

:

```sql
SELECT p.id, p.name, count(j.id) AS job_count
FROM app.projects p
LEFT JOIN app.jobs j ON j.project_id = p.id
GROUP BY p.id, p.name;
```

---

## 次のステップ

- 上記を基にマイグレーションスクリプト（SQL ファイルまたはマイグレーションツール用のファイル）を作成する。
- アプリケーションコード（`src/`）と型/モデルの整合性を確認する（models のフィールドと DB スキーマを合わせる）。
- 必要ならパフォーマンスの想定負荷に基づくパーティショニング設計を行う。

---

:: 用語
- JSONB: PostgreSQL の JSON 型。構造化データの柔軟な保存に便利。GIN インデックスを利用可能。
- CONCURRENTLY: インデックス作成をテーブルロックせずに行える。ただし同時に他の CREATE INDEX CONCURRENTLY はできない。

