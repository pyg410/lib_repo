# LiteLLM 1.93.0용 Node.js 26 오프라인 APK 수집

대상: Wolfi / x86_64. 조사일: 2026-10-27~28 (Asia/Seoul).

**설치 준비 완료 번들이 아닙니다.** 공식 저장소에서 받은 APK 20개 모두 `.SIGN.*` 항목이 없으며,
공식 Wolfi 키를 이용한 `apk verify` 결과가 `UNTRUSTED`입니다.
APKINDEX 자체의 서명 검증은 `OK`입니다. 다운로드 SHA256은 무결성 확인용이며 서명을 대체하지 않습니다.
서명 우회, APK 수정·재패키징, OpenSSL 3 제거·업그레이드는 수행하지 않았습니다.
이 상태를 명시하기 위해 Release는 prerelease로 게시합니다.

Release: https://github.com/pyg410/lib_repo/releases/tag/litellm-node26-offline

## 출처와 확인 결과

- 저장소: https://packages.wolfi.dev/os/x86_64/
- 인덱스: https://packages.wolfi.dev/os/x86_64/APKINDEX.tar.gz
- 공식 키: https://packages.wolfi.dev/os/wolfi-signing.rsa.pub
- Node: `nodejs-26=26.12.1-r2` 정확히 확보. 대체 버전 없음.
- `openssl-4.0-libcrypto=4.0.3-r8`: `usr/lib/libcrypto.so.4` 포함.
- `openssl-4.0-libssl=4.0.3-r8`: `usr/lib/libssl.so.4` 포함.
- 모든 APK의 크기, `.PKGINFO` 이름·버전·아키텍처·의존성을 APKINDEX와 대조함.
- `apk add --simulate`를 빈 APK 데이터베이스에 적용하여 아래 20개 의존성 폐쇄 집합을 산출함.
- `apk fetch --recursive`는 패키지 선택 오류로 실패하여, 설치 시뮬레이션이 선택한 고정 버전을 직접 다운로드함.
- 모든 APK는 Wolfi 공식 URL에서 그대로 받았으며 Alpine APK를 포함하지 않음.

## 실제 검증

고정된 검증 도구 이미지:
`cgr.dev/chainguard/wolfi-base@sha256:0b179206ab162b12a43bacea1b525a4023e0272005c92d08555c61b1beaedc40`

Docker `--platform linux/amd64 --network none` 환경에서 `apk-tools 2.14.10` 사용.
이미지의 Wolfi 키와 공식 URL의 키가 바이트 단위로 일치함.
`apk verify`는 인덱스만 통과하고 APK 20개를 모두 `UNTRUSTED`로 판정함.
서명 우회 옵션 없이 빈 루트에 아래 명령을 실제 실행했으나 서명 신뢰 오류로 실패함:

```sh
apk --root /tmp/offline-root --arch x86_64 --initdb \
  --keys-dir /work/keys --repositories-file /dev/null \
  add --no-network /work/apks/*.apk
```

**오프라인 설치 성공 및 Node 실행은 검증되지 않았습니다.** LiteLLM 1.93.0 실제 대상 이미지에서도 검증되지 않았습니다.
서명된 원본 APK를 확보한 뒤 동일한 검증을 다시 통과해야 합니다.
`--allow-untrusted`, `--force-overwrite` 등 우회 옵션은 사용하지 않습니다.

OpenSSL 4 라이브러리의 SONAME은 OpenSSL 3와 다르지만, libcrypto 패키지가
`/etc/ssl/openssl.cnf`, `/etc/ssl/ca.cnf`도 포함하고 legacy provider가 공용 경로를 포함합니다.
따라서 대상 이미지의 기존 패키지와 파일 소유권 충돌 여부는 별도로 확인해야 합니다.
이 의존성 집합은 빈 루트 기준이며 기존 회사 이미지에 무조건 일괄 설치·업그레이드할 목록이 아닙니다.

## 재수집

Python 3, curl, Docker가 필요합니다. 출력 위치는 Git 저장소 밖으로 지정합니다.

```sh
python3 download.py /tmp/litellm-node26-download
```

스크립트는 현재 공식 인덱스에 고정 항목이 존재하는지 확인하고 원본 APK의 기록된 SHA256,
메타데이터, 공식 키를 검증합니다. 버전·내용이 달라지면 중단하며 대체하지 않습니다.
서명 확인 실패 시 파일·체크섬·로그를 보존하고 종료 코드 2를 반환합니다.
자동 설치나 Release 업로드는 하지 않습니다.

폐쇄망으로 전달한 파일은 `sha256sum -c SHA256SUMS.txt`로 확인할 수 있습니다.
다만 현재 파일은 서명 검증에 실패하므로 운영 환경 설치를 진행하지 마십시오.
공식 키 신뢰는 별도의 신뢰된 경로로 확인해야 합니다.

## 패키지 명세

모든 행의 서명 상태: **UNSIGNED / UNTRUSTED**.

| 패키지 | 버전 | 원본 다운로드 URL |
|---|---|---|
| `ca-certificates-bundle` | `20261020-r0` | [ca-certificates-bundle-20261020-r0.apk](https://packages.wolfi.dev/os/x86_64/ca-certificates-bundle-20261020-r0.apk) |
| `wolfi-baselayout` | `20230201-r30` | [wolfi-baselayout-20230201-r30.apk](https://packages.wolfi.dev/os/x86_64/wolfi-baselayout-20230201-r30.apk) |
| `glibc-2.44-locale-posix` | `2.44-r10` | [glibc-2.44-locale-posix-2.44-r10.apk](https://packages.wolfi.dev/os/x86_64/glibc-2.44-locale-posix-2.44-r10.apk) |
| `libgcc` | `16.2.0-r2` | [libgcc-16.2.0-r2.apk](https://packages.wolfi.dev/os/x86_64/libgcc-16.2.0-r2.apk) |
| `glibc-2.44` | `2.44-r10` | [glibc-2.44-2.44-r10.apk](https://packages.wolfi.dev/os/x86_64/glibc-2.44-2.44-r10.apk) |
| `ld-linux-2.44` | `2.44-r10` | [ld-linux-2.44-2.44-r10.apk](https://packages.wolfi.dev/os/x86_64/ld-linux-2.44-2.44-r10.apk) |
| `libbrotlicommon1` | `1.2.1-r2` | [libbrotlicommon1-1.2.1-r2.apk](https://packages.wolfi.dev/os/x86_64/libbrotlicommon1-1.2.1-r2.apk) |
| `libbrotlidec1` | `1.2.1-r2` | [libbrotlidec1-1.2.1-r2.apk](https://packages.wolfi.dev/os/x86_64/libbrotlidec1-1.2.1-r2.apk) |
| `libbrotlienc1` | `1.2.1-r2` | [libbrotlienc1-1.2.1-r2.apk](https://packages.wolfi.dev/os/x86_64/libbrotlienc1-1.2.1-r2.apk) |
| `c-ares` | `1.34.9-r0` | [c-ares-1.34.9-r0.apk](https://packages.wolfi.dev/os/x86_64/c-ares-1.34.9-r0.apk) |
| `openssl-provider-legacy-allowed` | `4.1.0-r0` | [openssl-provider-legacy-allowed-4.1.0-r0.apk](https://packages.wolfi.dev/os/x86_64/openssl-provider-legacy-allowed-4.1.0-r0.apk) |
| `openssl-4.0-libcrypto` | `4.0.3-r8` | [openssl-4.0-libcrypto-4.0.3-r8.apk](https://packages.wolfi.dev/os/x86_64/openssl-4.0-libcrypto-4.0.3-r8.apk) |
| `icu78-data-full` | `78.3-r4` | [icu78-data-full-78.3-r4.apk](https://packages.wolfi.dev/os/x86_64/icu78-data-full-78.3-r4.apk) |
| `libstdc++` | `16.2.0-r2` | [libstdc++-16.2.0-r2.apk](https://packages.wolfi.dev/os/x86_64/libstdc++-16.2.0-r2.apk) |
| `libicu78` | `78.3-r4` | [libicu78-78.3-r4.apk](https://packages.wolfi.dev/os/x86_64/libicu78-78.3-r4.apk) |
| `libnghttp2-14` | `1.70.0-r7` | [libnghttp2-14-1.70.0-r7.apk](https://packages.wolfi.dev/os/x86_64/libnghttp2-14-1.70.0-r7.apk) |
| `openssl-4.0-libssl` | `4.0.3-r8` | [openssl-4.0-libssl-4.0.3-r8.apk](https://packages.wolfi.dev/os/x86_64/openssl-4.0-libssl-4.0.3-r8.apk) |
| `libuv` | `1.53.0-r0` | [libuv-1.53.0-r0.apk](https://packages.wolfi.dev/os/x86_64/libuv-1.53.0-r0.apk) |
| `zlib` | `1.3.2.1_rc20260921-r1` | [zlib-1.3.2.1_rc20260921-r1.apk](https://packages.wolfi.dev/os/x86_64/zlib-1.3.2.1_rc20260921-r1.apk) |
| `nodejs-26` | `26.12.1-r2` | [nodejs-26-26.12.1-r2.apk](https://packages.wolfi.dev/os/x86_64/nodejs-26-26.12.1-r2.apk) |

### APKINDEX 의존성과 제공 항목

- **ca-certificates-bundle=20261020-r0**
  - 의존성: `merged-usrsbin wolfi-baselayout`
  - 제공: `(없음)`
- **wolfi-baselayout=20230201-r30**
  - 의존성: `ca-certificates-bundle`
  - 제공: `merged-bin merged-lib merged-sbin merged-usrsbin merged-varrun`
- **glibc-2.44-locale-posix=2.44-r10**
  - 의존성: `merged-lib merged-sbin merged-usrsbin wolfi-baselayout`
  - 제공: `glibc-locale-posix=2.44-r10`
- **libgcc=16.2.0-r2**
  - 의존성: `so:ld-linux-x86-64.so.2 so:libc.so.6`
  - 제공: `libgcc-16=16.2.0-r2 so-ver:libgcc_s.so.1=16.2.0-r2 so:libgcc_s.so.1=1`
- **glibc-2.44=2.44-r10**
  - 의존성: `!musl glibc-2.44-locale-posix ld-linux-2.44=2.44-r10 libgcc merged-lib merged-sbin merged-usrsbin so:ld-linux-x86-64.so.2 wolfi-baselayout`
  - 제공: `cmd:ldconfig=2.44-r10 glibc=2.44-r10 so-ver:libBrokenLocale.so.1=2.44-r10 so-ver:libanl.so.1=2.44-r10 so-ver:libc.so.6=2.44-r10 so-ver:libc_malloc_debug.so.0=2.44-r10 so-ver:libdl.so.2=2.44-r10 so-ver:libm.so.6=2.44-r10 so-ver:libmemusage.so=2.44-r10 so-ver:libmvec.so.1=2.44-r10 so-ver:libnsl.so.1=2.44-r10 so-ver:libnss_compat.so.2=2.44-r10 so-ver:libnss_dns.so.2=2.44-r10 so-ver:libnss_files.so.2=2.44-r10 so-ver:libpthread.so.0=2.44-r10 so-ver:libresolv.so.2=2.44-r10 so-ver:librt.so.1=2.44-r10 so-ver:libthread_db.so.1=2.44-r10 so-ver:libutil.so.1=2.44-r10 so:libBrokenLocale.so.1=1 so:libanl.so.1=1 so:libc.so.6=6 so:libc_malloc_debug.so.0=0 so:libdl.so.2=2 so:libm.so.6=6 so:libmemusage.so=0 so:libmvec.so.1=1 so:libnsl.so.1=1 so:libnss_compat.so.2=2 so:libnss_dns.so.2=2 so:libnss_files.so.2=2 so:libpthread.so.0=0 so:libresolv.so.2=2 so:librt.so.1=1 so:libthread_db.so.1=1 so:libutil.so.1=1`
- **ld-linux-2.44=2.44-r10**
  - 의존성: `glibc-2.44=2.44-r10 merged-lib merged-sbin merged-usrsbin wolfi-baselayout`
  - 제공: `ld-linux=2.44-r10 so-ver:ld-linux-x86-64.so.2=2.44-r10 so:ld-linux-x86-64.so.2=2`
- **libbrotlicommon1=1.2.1-r2**
  - 의존성: `so:libc.so.6`
  - 제공: `so-ver:libbrotlicommon.so.1=1.2.1-r2 so:libbrotlicommon.so.1=1`
- **libbrotlidec1=1.2.1-r2**
  - 의존성: `so:libbrotlicommon.so.1 so:libc.so.6`
  - 제공: `so-ver:libbrotlidec.so.1=1.2.1-r2 so:libbrotlidec.so.1=1`
- **libbrotlienc1=1.2.1-r2**
  - 의존성: `so:libbrotlicommon.so.1 so:libc.so.6 so:libm.so.6`
  - 제공: `so-ver:libbrotlienc.so.1=1.2.1-r2 so:libbrotlienc.so.1=1`
- **c-ares=1.34.9-r0**
  - 의존성: `so:libc.so.6`
  - 제공: `so-ver:libcares.so.2=1.34.9-r0 so:libcares.so.2=2`
- **openssl-provider-legacy-allowed=4.1.0-r0**
  - 의존성: `so:libc.so.6`
  - 제공: `(없음)`
- **openssl-4.0-libcrypto=4.0.3-r8**
  - 의존성: `openssl-provider-legacy-allowed so:libbrotlidec.so.1 so:libbrotlienc.so.1 so:libc.so.6`
  - 제공: `so-ver:libcrypto.so.4=4.0.3-r8 so:libcrypto.so.4=4`
- **icu78-data-full=78.3-r4**
  - 의존성: `(없음)`
  - 제공: `(없음)`
- **libstdc++=16.2.0-r2**
  - 의존성: `so:ld-linux-x86-64.so.2 so:libc.so.6 so:libgcc_s.so.1 so:libm.so.6`
  - 제공: `libstdc++-16=16.2.0-r2 so-ver:libstdc++.so.6=16.2.0-r2 so:libstdc++.so.6=6`
- **libicu78=78.3-r4**
  - 의존성: `icu78-data-full so:ld-linux-x86-64.so.2 so:libc.so.6 so:libgcc_s.so.1 so:libm.so.6 so:libstdc++.so.6`
  - 제공: `so-ver:libicudata.so.78=78.3-r4 so-ver:libicui18n.so.78=78.3-r4 so-ver:libicuio.so.78=78.3-r4 so-ver:libicuuc.so.78=78.3-r4 so:libicudata.so.78=78 so:libicui18n.so.78=78 so:libicuio.so.78=78 so:libicuuc.so.78=78`
- **libnghttp2-14=1.70.0-r7**
  - 의존성: `so:libc.so.6`
  - 제공: `so-ver:libnghttp2.so.14=1.70.0-r7 so:libnghttp2.so.14=14`
- **openssl-4.0-libssl=4.0.3-r8**
  - 의존성: `so:libc.so.6 so:libcrypto.so.4`
  - 제공: `so-ver:libssl.so.4=4.0.3-r8 so:libssl.so.4=4`
- **libuv=1.53.0-r0**
  - 의존성: `so:libc.so.6`
  - 제공: `so-ver:libuv.so.1=1.53.0-r0 so:libuv.so.1=1`
- **zlib=1.3.2.1_rc20260921-r1**
  - 의존성: `merged-lib so:libc.so.6 wolfi-baselayout`
  - 제공: `so-ver:libz.so.1=1.3.2.1_rc20260921-r1 so:libz.so.1=1`
- **nodejs-26=26.12.1-r2**
  - 의존성: `so:ld-linux-x86-64.so.2 so:libbrotlidec.so.1 so:libbrotlienc.so.1 so:libc.so.6 so:libcares.so.2 so:libcrypto.so.4 so:libgcc_s.so.1 so:libicui18n.so.78 so:libicuuc.so.78 so:libm.so.6 so:libnghttp2.so.14 so:libssl.so.4 so:libstdc++.so.6 so:libuv.so.1 so:libz.so.1`
  - 제공: `cmd:node=26.12.1-r2 nodejs=26.12.1-r2`

## Release 파일

위 표의 APK 20개와 다음 6개 파일을 첨부합니다.

- `SHA256SUMS.txt`: 나머지 모든 Release Asset의 SHA256
- `README.md`: 이 문서
- `APKINDEX.tar.gz`: 공식 인덱스 원본 스냅샷
- `wolfi-signing.rsa.pub`: 공식 Wolfi 공개키
- `signature-verification.txt`: 서명 검증 로그
- `install-verification.txt`: 실제 오프라인 설치 실패 로그

Git에는 `download.py`와 `README.md`만 커밋합니다. APK 및 검증 자료는 Release Assets에만 게시합니다.
