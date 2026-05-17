# Agent Handoff — tiferet-monday v1.x

**Date:** 2026-05-17  
**Last Agent Session:** v1.0.0a1 alpha release  
**Repository:** https://github.com/greatstrength/tiferet-monday  

## Current State

### Branches
- **`v1.x-proto`** — Long-lived prototype branch (plan lives here conceptually).
- **`v1.0b1-release`** — Active release branch. All implementation work happens from feature branches off this branch.
- **Tag `v1.0.0a1`** — First alpha release, pushed to origin. Contains the full Phase 1+2 foundation.

### What Was Completed (Phase 1 + Phase 2)

The entire package was rewritten from the legacy v0.2 architecture to the v1.x DDD architecture. **All code is on `v1.0b1-release` at tag `v1.0.0a1`.**

**8 packages implemented:**

| Package | Purpose | Key Files |
|---|---|---|
| `assets/` | Constants, error codes | `constants.py` |
| `utils/` | GraphQL builder (from moncli) | `graphql.py` — `GraphQLField`, `GraphQLOperation`, `ArgumentValue`, `InlineFragment` |
| `domain/` | Read-only domain objects (Pydantic v2) | `settings.py`, `board.py` (Board, Column, Group), `item.py` (Item, Update, Reply), `column_value.py` (15 typed subclasses with `Literal` discriminators) |
| `mappers/` | API response → domain mapping | `settings.py` (MondayObject base), `column_value.py` (registry + discriminated union + `_GRAPHQL_FRAGMENT` alignment) |
| `interfaces/` | Service ABCs | `settings.py` (MondayService), `board.py` (BoardService, 9 methods), `item.py` (ItemService, 10 methods) |
| `events/` | Domain events | `settings.py` (MondayEvent with retry), `board.py` (6 events), `item.py` (7 events) |
| `repos/` | Concrete API proxies | `settings.py` (MondayApiProxy + MondayApiError), `board.py` (BoardApiProxy), `item.py` (ItemApiProxy) |
| `contexts/` | Context-as-client pattern | `settings.py` (MondayContext), `app.py` (MondayApp), `board.py` (BoardContext), `item.py` (ItemContext) |

### Key Architecture Decisions

1. **Context-as-Client Pattern:** `MondayApp.get_board(id)` returns a `BoardContext` that wraps a `Board` domain object and exposes methods like `get_items()`, `create_item()`, `get_columns()` — each triggering domain events internally.

2. **Column Value Discriminated Unions:** `mappers/column_value.py` uses a `@monday_column_type('status')` decorator to self-register MondayObject subclasses. The `ColumnValueType` discriminated union auto-dispatches raw API dicts to the correct typed class. Unknown types fall back to `ColumnValueMondayObject`. 15 types registered, 14 have `_GRAPHQL_FRAGMENT` for dynamic query assembly.

3. **MondayObject (not YamlObject):** Transfer objects use the `MondayObject` suffix since data comes from the Monday.com GraphQL API (JSON), not YAML config files.

4. **GraphQL Builder:** `utils/graphql.py` adapts moncli's `GraphQLField`/`GraphQLOperation` for composable query construction. Currently the repos still use raw query strings — a future pass could refactor them to use the builder.

5. **Complexity Budget Retry:** `MondayApiProxy._handle_response()` detects `COMPLEXITY_BUDGET_EXHAUSTED` errors and raises `MondayApiError` with retry seconds. `MondayEvent.handle_with_retry()` provides the retry loop.

### Validation
- All imports chain cleanly: `from tiferet_monday import MondayApp, BoardContext, ItemContext, MondayApiError`
- `MondayApp(api_key='test')` instantiates correctly with `BoardApiProxy` and `ItemApiProxy`
- Column value discriminated union dispatches 15 types + default fallback
- Version: `1.0.0a1`

## What Remains (Phases 3–5)

Refer to the **implementation plan** (plan artifact `e7d33af1-0589-4eeb-a332-40f26e5b53ed`) for the full API coverage matrix and phased approach.

### Phase 3: Secondary Domains
Each domain follows the same layered pattern: `domain/` → `mappers/` → `interfaces/` → `events/` → `repos/` → `contexts/`.

- **Updates & Notifications** — `domain/update.py` already has `Update`/`Reply`; needs its own `UpdateService`, `UpdateApiProxy`, and optionally `UpdateContext`. Also `create_notification` mutation.
- **Docs** — `domain/doc.py` (Document, DocumentBlock), `DocumentService`, `DocumentApiProxy`, `DocumentContext`. The v0.2 had these; need to be rebuilt in v1.x style.
- **Users & Teams** — `domain/user.py` (User, Team, Account), `UserService`, `UserApiProxy`, `UserContext`. `MondayApp` needs `get_users()`, `get_me()`, `get_teams()`.

### Phase 4: Tertiary Domains
- **Workspaces** — `domain/workspace.py` (Workspace, Folder), full CRUD.
- **Assets** — `domain/asset.py`, file upload support.
- **Tags** — `domain/tag.py`, `create_or_get_tag`.
- **Webhooks** — `domain/webhook.py`, `create_webhook`/`delete_webhook`.
- **Board Subscribers** — add/remove subscriber mutations to `BoardService`.

### Phase 5: Testing & Polish
- Unit tests for domain events (mock services, validate dispatch).
- Integration tests with mock API responses.
- Expand column value coverage to remaining Monday types: `tags`, `color_picker`, `country`, `formula`, `mirror`, `connect_boards`, `dependency`, `time_tracking`, `vote`, `world_clock`, `creation_log`, `last_updated`.
- Refactor repos to use `utils/graphql.py` builder instead of raw query strings.
- Documentation and usage examples.

## Reference Material

- **moncli** is cloned at `/Users/ashatz/Documents/GitHub/moncli` — useful for column value types (`moncli/column_value/`), entity patterns (`moncli/entities/`), and GraphQL construction (`moncli/api_v2/graphql.py`). Do NOT copy moncli conventions; adapt to Tiferet patterns.
- **Monday.com API Reference:** https://developer.monday.com/api-reference — 49 operations across boards, items, columns, groups, workspaces, docs, users, teams, updates, notifications, assets, tags, webhooks, dashboards, forms.
- **Tiferet Rules:** The user has extensive Tiferet framework rules (structured code style, domain objects, events, interfaces, mappers, utilities). Follow these strictly.

## How to Add a New Domain

Example: adding the Users domain.

1. **`domain/user.py`** — Define `User(MondayDomainObject)`, `Team(MondayDomainObject)`, `Account(MondayDomainObject)`.
2. **`mappers/user.py`** — Define `UserMondayObject(User, MondayObject)`, etc.
3. **`interfaces/user.py`** — Define `UserService(MondayService)` with abstract methods (`get_users`, `get_me`, `get_teams`, `get_account`).
4. **`events/user.py`** — Define `GetUsers(MondayEvent)`, `GetMe(MondayEvent)`, etc.
5. **`repos/user.py`** — Define `UserApiProxy(UserService, MondayApiProxy)` with GraphQL queries.
6. **`contexts/user.py`** — Define `UserContext(MondayContext)` wrapping `User` domain object.
7. **`contexts/settings.py`** — Add `_user_service` to `MondayContext`.
8. **`contexts/app.py`** — Add `get_users()`, `get_me()` methods to `MondayApp`.
9. Update `__init__.py` exports.

## Virtual Environment
- Located at `.venv/` in the project root.
- Activate with `source .venv/bin/activate`.
- Dependencies: `tiferet>=1.1.1`, `requests>=2.32.4`, `pydantic>=2.0.0`.
