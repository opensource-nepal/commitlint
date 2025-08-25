# CHANGELOG

## [1.3.1](https://github.com/opensource-nepal/commitlint/compare/v1.3.0...v1.3.1) (2025-08-25)


### Bug Fixes

* add github api failed response ([#72](https://github.com/opensource-nepal/commitlint/issues/72)) ([e3ae577](https://github.com/opensource-nepal/commitlint/commit/e3ae577534c63cd89624e60a9e4257a0b1eee148))

## [1.3.0](https://github.com/opensource-nepal/commitlint/compare/v1.2.0...v1.3.0) (2024-08-30)


### Features

* enhanced actions logging with clear annotations ([#61](https://github.com/opensource-nepal/commitlint/issues/61)) ([7f72e91](https://github.com/opensource-nepal/commitlint/commit/7f72e9108526ef0f05afcb1627d1239ed41324c6))


### Bug Fixes

* fix major version tag fetch on pre-commit autoupdate ([#65](https://github.com/opensource-nepal/commitlint/issues/65)) ([dffb36b](https://github.com/opensource-nepal/commitlint/commit/dffb36bf7774910ae14417f57b22a12ff0cb323b))

## [1.2.0](https://github.com/opensource-nepal/commitlint/compare/v1.1.0...v1.2.0) (2024-07-24)


### Features

* allow bump commits ([#55](https://github.com/opensource-nepal/commitlint/issues/55)) ([bb8a3b7](https://github.com/opensource-nepal/commitlint/commit/bb8a3b74134f42a48acec18ab87e6a0293c07e84))


### Bug Fixes

* handle commit message starting with # ([#59](https://github.com/opensource-nepal/commitlint/issues/59)) ([ea7683f](https://github.com/opensource-nepal/commitlint/commit/ea7683f2cf265090fda7ddfadfc9853caa05e546))

## [1.1.0](https://github.com/opensource-nepal/commitlint/compare/v1.0.0...v1.1.0) (2024-07-02)


### Features

* support pull_request_target events ([#52](https://github.com/opensource-nepal/commitlint/issues/52)) ([62e1128](https://github.com/opensource-nepal/commitlint/commit/62e11285d5628dff5f67645d1c718e1276478ecb))


### Bug Fixes

* security updates on commitlint action and workflows ([#48](https://github.com/opensource-nepal/commitlint/issues/48)) ([b98c73f](https://github.com/opensource-nepal/commitlint/commit/b98c73fb68f11b66ec8d3f227c6b129598c28726))

## [1.0.0](https://github.com/opensource-nepal/commitlint/compare/v0.2.1...v1.0.0) (2024-05-24)


### Features

* Add fail_on_error github action parameter ([00bf73f](https://github.com/opensource-nepal/commitlint/commit/00bf73fef7120ceb335dc9ef84a4390a2d1ccb59))
* add verbose option ([4ec08c1](https://github.com/opensource-nepal/commitlint/commit/4ec08c1cd2f22a67bbfa1fc9ef490ca7f5b1800e))
* added error annotation on github actions ([830de67](https://github.com/opensource-nepal/commitlint/commit/830de67d92356085663cd23e5e79c1522b23901e))
* **cli:** added the quiet option in cli ([b1778c8](https://github.com/opensource-nepal/commitlint/commit/b1778c8dead03eaba7625c67f741e185be19ea49))
* enhanced error message ([9a8c081](https://github.com/opensource-nepal/commitlint/commit/9a8c08173abd3086d14fe4142736d9bfb93ef08f))
* show version info [#13](https://github.com/opensource-nepal/commitlint/issues/13) ([0a5f9c1](https://github.com/opensource-nepal/commitlint/commit/0a5f9c1e29b8a7beaf4a9a5ce1991935f84e9c7d))


### Bug Fixes

* handle the file not found error gracefully ([#46](https://github.com/opensource-nepal/commitlint/issues/46)) ([6c5a65c](https://github.com/opensource-nepal/commitlint/commit/6c5a65c222963f713379739f57273b82cac1a0b0))


### Documentation

* update usage information for v1 ([03d7b5b](https://github.com/opensource-nepal/commitlint/commit/03d7b5ba370532f39b42ae9f2148f7ed08cbb826))

## 0.2.1

- Update Github actions name.
- Updated documentations for Github actions and pre-commit hook.

## 0.2.0

- Created commitlint CLI.
- Created pre-commit configuration for `commit-msg` hook.
- Created support for Github Actions.
