# Changelog

## [0.6.0](https://github.com/iloveitaly/beautiful-traceback/compare/v0.5.0...v0.6.0) (2026-02-10)


### Features

* **hook:** log overrides of non-default excepthooks ([222d6dc](https://github.com/iloveitaly/beautiful-traceback/commit/222d6dc8dbeee3d02a6d6cf4122e87e5a1cd72ec))
* **traceback:** include thread info for exceptions and hook thread excepthook ([d59579b](https://github.com/iloveitaly/beautiful-traceback/commit/d59579ba3d42b44a5b8ce12c2a06e6c6a39664ab))


### Bug Fixes

* stop supporting windows colorama logic ([d49a8eb](https://github.com/iloveitaly/beautiful-traceback/commit/d49a8eb049da99fa796b8a6e7969b63dc8f5064a))


### Documentation

* add json_demo and fastapi_demo with usage instructions ([b5d4e12](https://github.com/iloveitaly/beautiful-traceback/commit/b5d4e123636b084b40066e36edb6c90a6c7b1ebb))
* document automatic exception formatting for threads ([585fcd5](https://github.com/iloveitaly/beautiful-traceback/commit/585fcd53c254ba0da476a6e1cacf07da0fe8528a))
* document threading example and thread exception support ([9150091](https://github.com/iloveitaly/beautiful-traceback/commit/9150091202b89ec2a0767829e734322b61c4dac9))
* **examples:** add threading demo showing exceptions in threads ([a7fb795](https://github.com/iloveitaly/beautiful-traceback/commit/a7fb79580b014cf10cdfa074cf1ded05bf9a3491))
* remove AGENT.md with coding and testing guidelines ([ad341db](https://github.com/iloveitaly/beautiful-traceback/commit/ad341dbdc36c894cf0fc3708d6a47301ae8acd84))
* update badges and add project template reference in readme ([e331932](https://github.com/iloveitaly/beautiful-traceback/commit/e33193255839e214988e75bc8d6ceb5d56281764))

## [0.5.0](https://github.com/iloveitaly/beautiful-traceback/compare/v0.4.0...v0.5.0) (2026-01-30)


### Features

* **pytest:** add exclude_patterns option for frame filtering ([a90b3e7](https://github.com/iloveitaly/beautiful-traceback/commit/a90b3e79a12f7880e818ca30223c3ea231c0a15d))


### Bug Fixes

* **pytest_plugin:** rename exclude_patterns ini option for clarity ([4207c75](https://github.com/iloveitaly/beautiful-traceback/commit/4207c75ba346604925939f8e44a681f6d536ffa3))


### Documentation

* add initial agent and command prompts for gemini and Claude ([5a13921](https://github.com/iloveitaly/beautiful-traceback/commit/5a139214c1074f94fa6e1cd47ae4adf1d80c6b8a))
* add local guideline to keep CLI simple ([56bef23](https://github.com/iloveitaly/beautiful-traceback/commit/56bef2305a08c86072618356104540b3d34137c2))
* clarify exclude pattern matching and supported formats ([7168d88](https://github.com/iloveitaly/beautiful-traceback/commit/7168d88b9574302fa97e3eb3476692c1a4f14379))
* remove custom coding rules, prompts and instructions files ([b268ad6](https://github.com/iloveitaly/beautiful-traceback/commit/b268ad6f10d19ff0cf2768b43bb84eeebd3d9724))

## [0.4.0](https://github.com/iloveitaly/beautiful-traceback/compare/v0.3.0...v0.4.0) (2026-01-27)


### Features

* **pytest:** enhance assertion error formatting with diffs ([1dbfff4](https://github.com/iloveitaly/beautiful-traceback/commit/1dbfff4811ca04d464e907163e42799c277db249))


### Bug Fixes

* **pytest_plugin:** improve extraction of assertion diff lines ([d0394d2](https://github.com/iloveitaly/beautiful-traceback/commit/d0394d225a19443198cd76130e595cd8f114f38b))

## [0.3.0](https://github.com/iloveitaly/beautiful-traceback/compare/v0.2.0...v0.3.0) (2026-01-20)


### Features

* **json_formatting:** add exc_to_json for structured error logging ([7c850d0](https://github.com/iloveitaly/beautiful-traceback/commit/7c850d08a5e4a18eea5f73a3b4d25340a5b4fd07))


### Documentation

* **examples:** add json and fastapi demos for exc_to_json ([5c1fcc0](https://github.com/iloveitaly/beautiful-traceback/commit/5c1fcc066cfba25a03d64736f91e613e2ff31569))

## [0.2.0](https://github.com/iloveitaly/beautiful-traceback/compare/v0.1.0...v0.2.0) (2025-11-10)


### Features

* implement PTH file injection ([#3](https://github.com/iloveitaly/beautiful-traceback/issues/3)) ([b4cb307](https://github.com/iloveitaly/beautiful-traceback/commit/b4cb307b85fdab95b3b2f6576793a55600bf4051))


### Bug Fixes

* format cli.py to pass linting checks ([#4](https://github.com/iloveitaly/beautiful-traceback/issues/4)) ([f6a1259](https://github.com/iloveitaly/beautiful-traceback/commit/f6a12598ac8b0d6e4d33849e4e825dd7ddd51877))


### Documentation

* Refactor README content for better readability ([e8ab686](https://github.com/iloveitaly/beautiful-traceback/commit/e8ab686c78f4ebdd22a2e583bfc8b947a834489b))
* Revise README for better readability and structure ([8014d11](https://github.com/iloveitaly/beautiful-traceback/commit/8014d11410728ed701a85f694a69869f52525092))
* update license link format in README.md ([8ae4d1d](https://github.com/iloveitaly/beautiful-traceback/commit/8ae4d1df69b679abdd10b4d3aa71afbb1c68c13c))

## 0.1.0 (2025-10-31)


### Features

* **build:** register beautiful_traceback as pytest plugin in pyproject.toml ([08221dc](https://github.com/iloveitaly/beautiful-traceback/commit/08221dc55b703dd057dd5a8057277f332ec736a0))


### Bug Fixes

* prevent infinite loop on exception circular references in exc_to_traceback_str ([40dc438](https://github.com/iloveitaly/beautiful-traceback/commit/40dc4384e12bd710b1da494b3a7642ed68234ad9))
* update traceback comparison image to webp in README ([8bf97f6](https://github.com/iloveitaly/beautiful-traceback/commit/8bf97f676de3968264e81be8dbf0195a041d6352))


### Documentation

* add AI-generated TODO list with backlog and priorities ([fd5b689](https://github.com/iloveitaly/beautiful-traceback/commit/fd5b689f5c48863230fb9e0e1c9e70b73c175004))
* add coding rules and prompts for dev and backend standards ([72bfbb7](https://github.com/iloveitaly/beautiful-traceback/commit/72bfbb74e9dba59e84bb899600a461d5de1a69db))
* add MIT license to LICENSE.md ([4b36d59](https://github.com/iloveitaly/beautiful-traceback/commit/4b36d59dd787109db0c6ded34788bd16f707c709))
* add original README for pretty-traceback ([cf563fe](https://github.com/iloveitaly/beautiful-traceback/commit/cf563fe9e12f77b558959e038fa972d9748d5459))
* add traceback comparison image and example script ([b5ff750](https://github.com/iloveitaly/beautiful-traceback/commit/b5ff750ae0880694ddb91102c520b4736974d64a))
* clarify use with structlog and link starter template ([5c6e772](https://github.com/iloveitaly/beautiful-traceback/commit/5c6e772da27ac69e3aaf7ff584e0497346f7d79f))
* complete critical TODOs and update progress in TODO-ai.md ([5d273a2](https://github.com/iloveitaly/beautiful-traceback/commit/5d273a28ef1c4e6cf18ea085b56a19c821f0038b))
* **examples:** add Python demo scripts and README for usage ([26d1a11](https://github.com/iloveitaly/beautiful-traceback/commit/26d1a11eb2df7180cd75faa440937b4a9a3fa9d8))
* expand README with quickstart, IDE integration, and config info ([1764ba6](https://github.com/iloveitaly/beautiful-traceback/commit/1764ba67bd7e8aea10a02bad8633e2c0014001e8))
* rewrite README with usage examples and FastAPI integration ([6751bd6](https://github.com/iloveitaly/beautiful-traceback/commit/6751bd69f226ed8763ba310d5ae2a8106cb1a559))
* update examples section and add global pth installation guide ([6b99e3d](https://github.com/iloveitaly/beautiful-traceback/commit/6b99e3d6653f2ca699ecb95fdeb60d14ca77f081))
* update TODOs and README to reflect completed tasks and simplify traceback example ([b943bcd](https://github.com/iloveitaly/beautiful-traceback/commit/b943bcd2be7d7b22847bcc4c5ffa4f7513352b43))
