# Changelog

## [2.4.2](https://github.com/ai4os/ai4-metadata/compare/v2.4.1...v2.4.2) (2025-11-10)


### Bug Fixes

* rename version to main ([960ec75](https://github.com/ai4os/ai4-metadata/commit/960ec75d54a1855a9b0ac9c7ed81f429c4186354))
* restore Python 3.10 support ([#63](https://github.com/ai4os/ai4-metadata/issues/63)) ([8770e84](https://github.com/ai4os/ai4-metadata/commit/8770e847aa86675f5d9069c929f90b031780a0ea))
* Update JSON-LD import URL for MLDCAT-AP context ([01434e1](https://github.com/ai4os/ai4-metadata/commit/01434e15bb370a2c63659ee658c445d41d469659))
* update typer dep ([297936c](https://github.com/ai4os/ai4-metadata/commit/297936cbaf4b3423153cbba739df975f49167e71))

## [2.4.1](https://github.com/ai4os/ai4-metadata/compare/v2.4.0...v2.4.1) (2025-07-23)


### Bug Fixes

* use registry in JSON validation ([7912af2](https://github.com/ai4os/ai4-metadata/commit/7912af244a85589aafd764ca7e68734bbd0d2da6))

## [2.4.0](https://github.com/ai4os/ai4-metadata/compare/v2.3.1...v2.4.0) (2025-06-26)


### Features

* add SKOS ttl files ([a25e88e](https://github.com/ai4os/ai4-metadata/commit/a25e88e16fc3211b82058626fa7c226804da619e))
* improve schema management and loading (WIP) ([08671a2](https://github.com/ai4os/ai4-metadata/commit/08671a22ba351860048b7fc649bf75a318556ec3))
* improve testing of MLDCAT-AP profile generation ([b1d8afa](https://github.com/ai4os/ai4-metadata/commit/b1d8afa6a7743fe91358cec6f1f91662693cb1bb))
* include initial mapping support for MLDCAT-AP ([9dc6e9c](https://github.com/ai4os/ai4-metadata/commit/9dc6e9cac3f98aad1a3c89635adc36da58b560bb))
* include JSON-LD Context file ([c8f2fd7](https://github.com/ai4os/ai4-metadata/commit/c8f2fd75a098894a5b19d6c5bcb8e127ec460ebf))
* include new metadata field links.self ([5043cc2](https://github.com/ai4os/ai4-metadata/commit/5043cc29a3f1be3cb9ea0fede0a609d7ed01fe2c))
* mark the usage of "validate" as deprecated ([8183c30](https://github.com/ai4os/ai4-metadata/commit/8183c30b841d7747d64337eca219fdae56d8330c))
* render vocabularies in docs ([c3c67df](https://github.com/ai4os/ai4-metadata/commit/c3c67df68988be88f9f42647ecefe80bd7a773c1))
* use definitions for resource configurations ([fa9028a](https://github.com/ai4os/ai4-metadata/commit/fa9028af9b8238cb39115b94320a58e5964f97bd))
* use versions also for JSON-LD context files ([4b706d5](https://github.com/ai4os/ai4-metadata/commit/4b706d59d5a3b42937b17f012cb583e519cce106))
* validating multiple files (CLI) is deprecated ([aa9fe1d](https://github.com/ai4os/ai4-metadata/commit/aa9fe1d9dbb654ca3bdcd3efa6b0e6297d8d02da))


### Bug Fixes

* add ids to entries in vocabulary ([e369189](https://github.com/ai4os/ai4-metadata/commit/e3691893a233b3208177f2c7e3f20db6626c2296))
* add RDF files links ([384c259](https://github.com/ai4os/ai4-metadata/commit/384c2595208584d2bb6897067f830ff420ebae5d))
* build correctly source path ([48f614a](https://github.com/ai4os/ai4-metadata/commit/48f614a9cfd98f72af128f636639d616f320a755))
* build correctly source path ([fe9c20e](https://github.com/ai4os/ai4-metadata/commit/fe9c20e715a5f535fae23b7ed0b8ad9098bf9d20))
* change base URL to use w3id.org namespace ([a645bad](https://github.com/ai4os/ai4-metadata/commit/a645badd07d807882ff1367f362d8d067a857a3a))
* change correct metadata schemata version ([92015b6](https://github.com/ai4os/ai4-metadata/commit/92015b6c379999b93b6b528b40eb46f809b41dce))
* change FIXME to NOTE in comment ([ca41cd4](https://github.com/ai4os/ai4-metadata/commit/ca41cd4139510abe986bdfcf2edf8d7d52cb7938))
* change source path for links ([87309c2](https://github.com/ai4os/ai4-metadata/commit/87309c2f81a8cb9e537df60de058cf33f4e19218))
* convert strings into objects ([1d652b0](https://github.com/ai4os/ai4-metadata/commit/1d652b096f310b239984c9f1b8c927fd5d5dbad5))
* correct list item IDs ([0094dd6](https://github.com/ai4os/ai4-metadata/commit/0094dd620077c695bb367585f48fb67c46ab63a8))
* ensure that URLs do not have double slashes using ([#51](https://github.com/ai4os/ai4-metadata/issues/51)) ([eaa83ba](https://github.com/ai4os/ai4-metadata/commit/eaa83ba6af3c85e4f64ce01220913a1854cb4e53)), closes [#50](https://github.com/ai4os/ai4-metadata/issues/50)
* explicitly set static path ([fa71f9f](https://github.com/ai4os/ai4-metadata/commit/fa71f9f5892248a22fe9dd1be6b18ae9ed2e1da1))
* fix missing command entry points ([3cc8dad](https://github.com/ai4os/ai4-metadata/commit/3cc8dadbada749eec65cdeb19117eea5e25f8ab9))
* fix wrong version values in enums ([5d36c91](https://github.com/ai4os/ai4-metadata/commit/5d36c9178e5fca35b1b4e542d6198aa09ecfc7fd))
* improve package and submodule loading ([564faf2](https://github.com/ai4os/ai4-metadata/commit/564faf2a95c6f253d0b44b292d5ab8db284e8caf)), closes [#43](https://github.com/ai4os/ai4-metadata/issues/43) [#42](https://github.com/ai4os/ai4-metadata/issues/42)
* license is not mandatory, but this does not meat it cannot be included ([e7bbdb7](https://github.com/ai4os/ai4-metadata/commit/e7bbdb798c4eb1452cafceefb4393dcf0176a865))
* move JSON and YAML assets into src directory ([fbbe288](https://github.com/ai4os/ai4-metadata/commit/fbbe288ebbcf373b7b48e0a16de0875449d7648a))
* remove 'en' from doc URLs ([3471a6d](https://github.com/ai4os/ai4-metadata/commit/3471a6df500230ce03f69f0fa752d8b8f36fb335))
* remove commmented code ([868752c](https://github.com/ai4os/ai4-metadata/commit/868752c59b7ca631c33c74e03e13546e13f891e0))
* remove non used files ([f5a7264](https://github.com/ai4os/ai4-metadata/commit/f5a7264d9d72f8ee55d13c1150247a8fb006c422))
* return correct JSON ([c72d3d7](https://github.com/ai4os/ai4-metadata/commit/c72d3d79810755813f696cce7f7761a681fe8c56)), closes [#41](https://github.com/ai4os/ai4-metadata/issues/41)
* take into account numbers when generating samples ([ccbaf53](https://github.com/ai4os/ai4-metadata/commit/ccbaf5354cf2a0db04f62d04aa781d7a5de8bb9a))
* transform values into objects ([602065b](https://github.com/ai4os/ai4-metadata/commit/602065b3fd483c3c01c68944d3c4b9fd55587cb3))
* update JSON-LD file ([8df43a1](https://github.com/ai4os/ai4-metadata/commit/8df43a1d579e5cc9d50fb904bea0e6083f206799))
* use correct links for schema definitions ([af73827](https://github.com/ai4os/ai4-metadata/commit/af73827befd22f3f59a1b90d17fe17c8fbcc6ad1))
* use correct static path ([32ba5dd](https://github.com/ai4os/ai4-metadata/commit/32ba5dd85f94ae9fa86c2c1ea209b83be67f6af2))
* use correct URL for JSON-LD ([f88a3bc](https://github.com/ai4os/ai4-metadata/commit/f88a3bc939a030bcb7f45f4567782ddda0dd6d3c)), closes [#46](https://github.com/ai4os/ai4-metadata/issues/46)
* use docutils nodes to render links ([51dc9fc](https://github.com/ai4os/ai4-metadata/commit/51dc9fc2b9b08c1d91151dbbea66ea823c69c9db))
* use master branch for mldcat profile ([f8d291b](https://github.com/ai4os/ai4-metadata/commit/f8d291b88d9b606768bfe1aeefb2f3b789a8b977))
* use mldcatap for profile and mldcat-ap for the command ([58816b3](https://github.com/ai4os/ai4-metadata/commit/58816b35c7f28e7735b568d27632fd948d8440d3)), closes [#47](https://github.com/ai4os/ai4-metadata/issues/47)
* use subcommands to perform mappings ([c619dcb](https://github.com/ai4os/ai4-metadata/commit/c619dcbb88955418e393777b8c30345c10346371)), closes [#44](https://github.com/ai4os/ai4-metadata/issues/44)


### Documentation

* add correct RDT config ([8433085](https://github.com/ai4os/ai4-metadata/commit/8433085ae1e0990e86e9c0d98b220f08270fbe65))
* add missing dependency ([e4c1135](https://github.com/ai4os/ai4-metadata/commit/e4c113590647fb63b273a424e79f2306aa9ad5df))
* Create initial documentation and build via RTD ([f833766](https://github.com/ai4os/ai4-metadata/commit/f833766e21b9dd0c781722d0bd6963765aa5c83f))
* include some plugin options ([237d7a8](https://github.com/ai4os/ai4-metadata/commit/237d7a83f64442cce5824df2c9f96d9ef59d267b))
* install ai4-metadata to build docs ([9c762fb](https://github.com/ai4os/ai4-metadata/commit/9c762fb8e7d044de66e6b9daf5c87662464506f3))
* remove wrong link ([68ebf08](https://github.com/ai4os/ai4-metadata/commit/68ebf084bbb3d9ee3ff7cf02e9681aa7e36f05f1))

## [2.3.1](https://github.com/ai4os/ai4-metadata/compare/v2.3.0...v2.3.1) (2025-03-05)


### Bug Fixes

* error when mapping schemas ([bcefd60](https://github.com/ai4os/ai4-metadata/commit/bcefd601867bcf41f261b1ae0e246a06a283ebed))
* fix mypy error ([53cae21](https://github.com/ai4os/ai4-metadata/commit/53cae21c8059c74a83270b80d789e43ecaee113f))
* handle errors with no path ([bf15bf6](https://github.com/ai4os/ai4-metadata/commit/bf15bf624cd52fb7c69a97c40c36dd239ecef17d))
* move inference resources to numeric ([76173e9](https://github.com/ai4os/ai4-metadata/commit/76173e9dcde552f65e5532f496aab4e199fba5d8))
* show faulty parameter in error message ([e33231e](https://github.com/ai4os/ai4-metadata/commit/e33231e4a49772f224e6c381d1fed9dfb99e26d0))

## [2.3.0](https://github.com/ai4os/ai4-metadata/compare/v2.2.1...v2.3.0) (2025-02-13)


### Features

* Include inference resources in metadata ([88c5be3](https://github.com/ai4os/ai4-metadata/commit/88c5be3a8981e5c21422a5430b64a3c80cd1d588))


### Bug Fixes

* change YAML example to be actually YAML ([3777b6e](https://github.com/ai4os/ai4-metadata/commit/3777b6e7986e01c16a9abceb929dd5b65f069b8b))
* set correct file permissions ([199bc90](https://github.com/ai4os/ai4-metadata/commit/199bc90650df964216ec8ad08e7e8f52aa6527ac))

## [2.2.1](https://github.com/ai4os/ai4-metadata/compare/v2.2.0...v2.2.1) (2024-11-11)


### Bug Fixes

* include help stings for each command ([6f70136](https://github.com/ai4os/ai4-metadata/commit/6f7013620bbfb2f9dc01fe40de30392db9b3f962))
* typer.Exit must be raised to abort the program ([c0f78e3](https://github.com/ai4os/ai4-metadata/commit/c0f78e3a777ebe10a348e135b2a0e7140b612113)), closes [#27](https://github.com/ai4os/ai4-metadata/issues/27)
* using add_typer creates a subcommand group ([555f1e2](https://github.com/ai4os/ai4-metadata/commit/555f1e2295740103fa3885bd8b76dfc20fa8aeb2))

## [2.2.0](https://github.com/ai4os/ai4-metadata/compare/v2.1.0...v2.2.0) (2024-08-22)


### Features

* validate also generated metadata ([a6559eb](https://github.com/ai4os/ai4-metadata/commit/a6559eb662c52a4e9597421367ce3d37a70bd033))


### Bug Fixes

* Enum should inherit also from str ([c2ac3d9](https://github.com/ai4os/ai4-metadata/commit/c2ac3d9641a781400aed1edcb6e43b269b90c802))


### Documentation

* update README with shields ([b79c567](https://github.com/ai4os/ai4-metadata/commit/b79c567bcabdcc0e7280e08d3b931a2cea47ac66))

## [2.1.0](https://github.com/ai4os/ai4-metadata/compare/v2.0.2...v2.1.0) (2024-08-22)


### Features

* add examples in V2 schemata ([5e37644](https://github.com/ai4os/ai4-metadata/commit/5e376448298f8369227a7e1ecfa7e4b8cad96499))
* allow loading YAML files ([03bc86f](https://github.com/ai4os/ai4-metadata/commit/03bc86f52b80d2862f9604688d51cf3f0b609dce)), closes [#12](https://github.com/ai4os/ai4-metadata/issues/12)
* generate empty metadata files ([f56c519](https://github.com/ai4os/ai4-metadata/commit/f56c5190dc34b2fa3f0180c2ad7d934e485dd907)), closes [#14](https://github.com/ai4os/ai4-metadata/issues/14)
* improve message formatting, using rich ([a0ce5c7](https://github.com/ai4os/ai4-metadata/commit/a0ce5c74105bcac8c867cce88652c1ab190464e1)), closes [#13](https://github.com/ai4os/ai4-metadata/issues/13)
* move to Typer for CLI implementation ([9a05025](https://github.com/ai4os/ai4-metadata/commit/9a05025b512322f4236aea708c73d176377a8de5)), closes [#15](https://github.com/ai4os/ai4-metadata/issues/15)


### Bug Fixes

* always put metadata version when generating ([36a3adc](https://github.com/ai4os/ai4-metadata/commit/36a3adcee76dd047b81fa1252a9bfe6059ed6480))
* invalid default for enum ([f8b703e](https://github.com/ai4os/ai4-metadata/commit/f8b703ecf7ef816e1b46a0c65264c480c0553ba2))
* refactor generator ([4c80fdb](https://github.com/ai4os/ai4-metadata/commit/4c80fdb52e7bcf0ed1193c83eab8b757cf639915))
* remove commented code ([3c65bb6](https://github.com/ai4os/ai4-metadata/commit/3c65bb693e78957270384b8ec6c18bf91f1c8376))


### Documentation

* add Zenodo link ([daa08ac](https://github.com/ai4os/ai4-metadata/commit/daa08ace7468463b849d413416978d33978c1241))
* improve README ([f60b910](https://github.com/ai4os/ai4-metadata/commit/f60b910942937f446357d78959d46e70e7fc4829))
* include EU notice ([77b0c4c](https://github.com/ai4os/ai4-metadata/commit/77b0c4cf9e950ee26e1fb1b410a31e58c20c2c31))

## [2.0.2](https://github.com/ai4os/ai4-metadata/compare/v2.0.1...v2.0.2) (2024-08-19)


### Miscellaneous Chores

* release 2.0.2 ([adac436](https://github.com/ai4os/ai4-metadata/commit/adac43662dc911874707e16840d65222d3438ac1))

## [2.0.1](https://github.com/ai4os/ai4-metadata/compare/v2.0.0...v2.0.1) (2024-08-12)


### Bug Fixes

* typo on Python classifier ([c36e40e](https://github.com/ai4os/ai4-metadata/commit/c36e40efa83cbb6055225cb2cdefade94c1ee6c3))

## [2.0.0](https://github.com/ai4os/ai4-metadata/compare/1.0.0...v2.0.0) (2024-08-12)


### ⚠ BREAKING CHANGES

* rename old package to ai4-metadata
* update model metadata schema

### Features

* add base model link ([24763ed](https://github.com/ai4os/ai4-metadata/commit/24763ed031d5c1f84c689e02062d6c09d01d3f83))
* add DOI field ([3e053a3](https://github.com/ai4os/ai4-metadata/commit/3e053a34a1330cfa1d04647716e0a54bf40ff153))
* add ID to schema version ([fe08b68](https://github.com/ai4os/ai4-metadata/commit/fe08b68101a5bf8f8f00aa9ec66a4a6c1cf1d19e))
* add metadata_version to schemata and add CLI option ([5ab9c0e](https://github.com/ai4os/ai4-metadata/commit/5ab9c0e6b0f9cd7710094e4d14850d59c13d8bd5))
* added tools into topics ([a5fbfba](https://github.com/ai4os/ai4-metadata/commit/a5fbfbadffdb31035d839b944c470081794d2d2b))
* additional categories, tasks and data-type ([fb095e1](https://github.com/ai4os/ai4-metadata/commit/fb095e1fa24fa699dced7752dac8f4cbf5033edb))
* description should be a string ([9b3df7c](https://github.com/ai4os/ai4-metadata/commit/9b3df7c5d5d601b2a3323280c8dc45d2d4dea02c))
* do not add a license in the metadata, as repo should have one ([410624b](https://github.com/ai4os/ai4-metadata/commit/410624b5c262c9de6a27c550b7a15de7a8c8da6c))
* docker_image should not be mandatory ([aa36fd5](https://github.com/ai4os/ai4-metadata/commit/aa36fd5e43f9df5ed32859184efe93435896a059))
* fail if keywords still exist ([b422091](https://github.com/ai4os/ai4-metadata/commit/b422091335ef75b28beef1c97bcbab4361b86cca))
* include migration tool ([263f4ef](https://github.com/ai4os/ai4-metadata/commit/263f4ef7577eb81ee20f1ac64d759c5f4a1d8916))
* license should be an enum ([605fa2d](https://github.com/ai4os/ai4-metadata/commit/605fa2d1b0e4577bf11997f195531ec3b5dd2abc))
* print some output for valid instances ([79708e1](https://github.com/ai4os/ai4-metadata/commit/79708e1008e120d7df2349e799bb6c80040d298c))
* rename old package to ai4-metadata ([e7544cf](https://github.com/ai4os/ai4-metadata/commit/e7544cf90590facd819b49bf3ae8dd6bc01d82fe))
* split keywords in three different attributes ([4d9b7ef](https://github.com/ai4os/ai4-metadata/commit/4d9b7ef847813d4178223f500c9eb9223cba3041))
* update model metadata schema ([4e4e7cd](https://github.com/ai4os/ai4-metadata/commit/4e4e7cd050ad23aa2a06cd4c0ddeb99e304c6e96))
* Use an array for dates ([9c4b47b](https://github.com/ai4os/ai4-metadata/commit/9c4b47b1b194e2baab2c0fe554964919b1d9608c))


### Bug Fixes

* add pattern and example to version field ([ec3635d](https://github.com/ai4os/ai4-metadata/commit/ec3635d8102950f6d4b7d9af61d89fe3db18033e))
* add unit testing skeleton ([ef56a6b](https://github.com/ai4os/ai4-metadata/commit/ef56a6bb29882dc9adc44e9b7525c840d0ac88a4))
* add user friendly identifiers ([797c5fa](https://github.com/ai4os/ai4-metadata/commit/797c5fa689b241b3c3ea6d7252e5e055dafcd549))
* change main to master branch ([1f9f2ae](https://github.com/ai4os/ai4-metadata/commit/1f9f2aee7a0276bc8304940d89def538395122cd))
* change release type to python ([b9d6b50](https://github.com/ai4os/ai4-metadata/commit/b9d6b5007989f1680dcdf1ded9c05e9549849717))
* dates should be created not creation ([96b876f](https://github.com/ai4os/ai4-metadata/commit/96b876f2bc2793984268163bb9130eec4d73e78f))
* dates should be updated, not update ([3a9cb53](https://github.com/ai4os/ai4-metadata/commit/3a9cb5391506a364a77d126120171e6c1b7c04e0))
* fix sample for V2 ([71fdd7c](https://github.com/ai4os/ai4-metadata/commit/71fdd7c5db72916b80393e07e4eb1dd5b3996dce))
* fix unit tests style ([6a79785](https://github.com/ai4os/ai4-metadata/commit/6a79785fc06c60f155fc3257c793a08056ba79ce))
* include JSON schemata files in package ([0bd033b](https://github.com/ai4os/ai4-metadata/commit/0bd033bc2522fc74dc0eba4de4ab6856c1dce5e5))
* make black happy ([1f715a5](https://github.com/ai4os/ai4-metadata/commit/1f715a58482b8559114c89869f383be11597e04b))
* merge strings ([e20d8f2](https://github.com/ai4os/ai4-metadata/commit/e20d8f202d719eacd518389118fd00ea9db02e44))
* phrases should end with a period ([4ebfd38](https://github.com/ai4os/ai4-metadata/commit/4ebfd387f4d7a75f1d52688299eca3b556a4efbd))
* remove redundant comments ([22a2181](https://github.com/ai4os/ai4-metadata/commit/22a21816be4a73ac7c7f392ebb53e6625ad2e957))
* restructure code, add unit tests ([8b2cc8c](https://github.com/ai4os/ai4-metadata/commit/8b2cc8ca87abfa36a17f6b2c3ab8297d37f34927))
* use not-required correctly ([d1ec930](https://github.com/ai4os/ai4-metadata/commit/d1ec93001eb410366bb767ebdd47699d051b3f17))
