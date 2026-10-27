#!/usr/bin/env python3
"""Download pinned, original Wolfi APKs. Exit 2 if signature verification fails."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile

BASE = "https://packages.wolfi.dev/os"
IMAGE = "cgr.dev/chainguard/wolfi-base@sha256:0b179206ab162b12a43bacea1b525a4023e0272005c92d08555c61b1beaedc40"
KEY_SHA256 = 'f0031424cf46f7db780ce63a45f0fd6aa6f85f601e6bb3b7a91fe3d4d5b7d2cc'
PACKAGES = json.loads('''
[
  {
    "C": "Q19P7fzB945PuRaQEnzg9napiRzKE=",
    "P": "ca-certificates-bundle",
    "V": "20261020-r0",
    "A": "x86_64",
    "S": "118541",
    "D": "merged-usrsbin wolfi-baselayout",
    "sha256": "f0bee352ca8f87c2c3ec1bdd459836f2afbb4874703e3a21888846ee08a96f71"
  },
  {
    "C": "Q1qyFV0NZAQAnaHoGFhRwUQlzoQC0=",
    "P": "wolfi-baselayout",
    "V": "20230201-r30",
    "A": "x86_64",
    "S": "13933",
    "D": "ca-certificates-bundle",
    "p": "merged-bin merged-lib merged-sbin merged-usrsbin merged-varrun",
    "sha256": "0544802d073dac63485309a64a1f533735580bbbaa18b83a59058676c040c2fb"
  },
  {
    "C": "Q18Q8aPdMpQzeqEe490BZv9an7jkU=",
    "P": "glibc-2.44-locale-posix",
    "V": "2.44-r10",
    "A": "x86_64",
    "S": "99259",
    "D": "merged-lib merged-sbin merged-usrsbin wolfi-baselayout",
    "p": "glibc-locale-posix=2.44-r10",
    "sha256": "cde156a940fed1fcddaa131435d8eddde50ae51b7de0defa7c9d9363d6560098"
  },
  {
    "C": "Q1ZiXgGGwe5h6UXD0/Zbd/7LKBpkw=",
    "P": "libgcc",
    "V": "16.2.0-r2",
    "A": "x86_64",
    "S": "112648",
    "D": "so:ld-linux-x86-64.so.2 so:libc.so.6",
    "p": "libgcc-16=16.2.0-r2 so-ver:libgcc_s.so.1=16.2.0-r2 so:libgcc_s.so.1=1",
    "sha256": "37e38f29f667c0c8c4c2c98747dfbe2c8c87dda2a9505fa51f0d53ab40c711b8"
  },
  {
    "C": "Q1MZbDS1vnGwDRHYrj7iPv9DtGbFs=",
    "P": "glibc-2.44",
    "V": "2.44-r10",
    "A": "x86_64",
    "S": "3168764",
    "D": "!musl glibc-2.44-locale-posix ld-linux-2.44=2.44-r10 libgcc merged-lib merged-sbin merged-usrsbin so:ld-linux-x86-64.so.2 wolfi-baselayout",
    "p": "cmd:ldconfig=2.44-r10 glibc=2.44-r10 so-ver:libBrokenLocale.so.1=2.44-r10 so-ver:libanl.so.1=2.44-r10 so-ver:libc.so.6=2.44-r10 so-ver:libc_malloc_debug.so.0=2.44-r10 so-ver:libdl.so.2=2.44-r10 so-ver:libm.so.6=2.44-r10 so-ver:libmemusage.so=2.44-r10 so-ver:libmvec.so.1=2.44-r10 so-ver:libnsl.so.1=2.44-r10 so-ver:libnss_compat.so.2=2.44-r10 so-ver:libnss_dns.so.2=2.44-r10 so-ver:libnss_files.so.2=2.44-r10 so-ver:libpthread.so.0=2.44-r10 so-ver:libresolv.so.2=2.44-r10 so-ver:librt.so.1=2.44-r10 so-ver:libthread_db.so.1=2.44-r10 so-ver:libutil.so.1=2.44-r10 so:libBrokenLocale.so.1=1 so:libanl.so.1=1 so:libc.so.6=6 so:libc_malloc_debug.so.0=0 so:libdl.so.2=2 so:libm.so.6=6 so:libmemusage.so=0 so:libmvec.so.1=1 so:libnsl.so.1=1 so:libnss_compat.so.2=2 so:libnss_dns.so.2=2 so:libnss_files.so.2=2 so:libpthread.so.0=0 so:libresolv.so.2=2 so:librt.so.1=1 so:libthread_db.so.1=1 so:libutil.so.1=1",
    "sha256": "3ef639d18f6987125cd9ca4c6f593811d5f4b34b0b936c609694bc5e8b66d08f"
  },
  {
    "C": "Q1PQF4s3+pIzQqeQnzB6URbLOS76w=",
    "P": "ld-linux-2.44",
    "V": "2.44-r10",
    "A": "x86_64",
    "S": "163102",
    "D": "glibc-2.44=2.44-r10 merged-lib merged-sbin merged-usrsbin wolfi-baselayout",
    "p": "ld-linux=2.44-r10 so-ver:ld-linux-x86-64.so.2=2.44-r10 so:ld-linux-x86-64.so.2=2",
    "sha256": "1eec08c207b306e6f46315ff8bc18b03e9256c4bc8c4f96e62ecfaa21a724259"
  },
  {
    "C": "Q1hR13/btAoHKw3piU/POT5y4GwS8=",
    "P": "libbrotlicommon1",
    "V": "1.2.1-r2",
    "A": "x86_64",
    "S": "85871",
    "D": "so:libc.so.6",
    "p": "so-ver:libbrotlicommon.so.1=1.2.1-r2 so:libbrotlicommon.so.1=1",
    "sha256": "fcc021ab88501ff5fcc1d74783df7f062bb7c260050565a9ca556db2537aedc5"
  },
  {
    "C": "Q1StgOWSmECA/XsKwXr9lNj6rRTiQ=",
    "P": "libbrotlidec1",
    "V": "1.2.1-r2",
    "A": "x86_64",
    "S": "49150",
    "D": "so:libbrotlicommon.so.1 so:libc.so.6",
    "p": "so-ver:libbrotlidec.so.1=1.2.1-r2 so:libbrotlidec.so.1=1",
    "sha256": "bf2619bf5ab853dc8617c5f42fbba87f1cf1bf32e580322e22d49564554c31f6"
  },
  {
    "C": "Q1sd/3jnUNRLQE1b2odCcgTMx/ORs=",
    "P": "libbrotlienc1",
    "V": "1.2.1-r2",
    "A": "x86_64",
    "S": "448468",
    "D": "so:libbrotlicommon.so.1 so:libc.so.6 so:libm.so.6",
    "p": "so-ver:libbrotlienc.so.1=1.2.1-r2 so:libbrotlienc.so.1=1",
    "sha256": "e916a6a52270b1bf7ae14ca61f5b9a9dda068149c352ae8bf1cf10489dfe2959"
  },
  {
    "C": "Q1q+mrnOSiDkvj5KgcADgvy4Iboao=",
    "P": "c-ares",
    "V": "1.34.9-r0",
    "A": "x86_64",
    "S": "162856",
    "D": "so:libc.so.6",
    "p": "so-ver:libcares.so.2=1.34.9-r0 so:libcares.so.2=2",
    "sha256": "0cebbfc82ad2b6f08c5193eed7800bfcf7eaa5efc556a981a9f8c7eec56b2630"
  },
  {
    "C": "Q1K5CR6PVd/wWU++lG1SG1MRrQkJA=",
    "P": "openssl-provider-legacy-allowed",
    "V": "4.1.0-r0",
    "A": "x86_64",
    "S": "364302",
    "D": "so:libc.so.6",
    "sha256": "ffd0efe415279f8814a6ace7db4841789bf7c91085b90202b7236c6cf70e988e"
  },
  {
    "C": "Q1W9piTcgyubhrducJCMM7+qErDxo=",
    "P": "openssl-4.0-libcrypto",
    "V": "4.0.3-r8",
    "A": "x86_64",
    "S": "2403081",
    "D": "openssl-provider-legacy-allowed so:libbrotlidec.so.1 so:libbrotlienc.so.1 so:libc.so.6",
    "p": "so-ver:libcrypto.so.4=4.0.3-r8 so:libcrypto.so.4=4",
    "sha256": "d10eb0f17414cf586f7681baa3a15b942e09e3cf570f5de2a6799650671e067c"
  },
  {
    "C": "Q1M2e+/1RvbhepGmmNgiOthCWPbYw=",
    "P": "icu78-data-full",
    "V": "78.3-r4",
    "A": "x86_64",
    "S": "14031220",
    "sha256": "05864995b3445b6eed42f3a3cfa3d158710fcf2da133d452c24e9b91b67dbf37"
  },
  {
    "C": "Q1TDYeh0Iq9Fjbp5cPck+zZfmDn14=",
    "P": "libstdc++",
    "V": "16.2.0-r2",
    "A": "x86_64",
    "S": "1267168",
    "D": "so:ld-linux-x86-64.so.2 so:libc.so.6 so:libgcc_s.so.1 so:libm.so.6",
    "p": "libstdc++-16=16.2.0-r2 so-ver:libstdc++.so.6=16.2.0-r2 so:libstdc++.so.6=6",
    "sha256": "91d46dc63af715208b8d1424909f4df7e30cbc2321afaa9dcd412476e0297ebd"
  },
  {
    "C": "Q1OwqgciyTxRn7l6Y6Vw6fqCq3WuA=",
    "P": "libicu78",
    "V": "78.3-r4",
    "A": "x86_64",
    "S": "3154330",
    "D": "icu78-data-full so:ld-linux-x86-64.so.2 so:libc.so.6 so:libgcc_s.so.1 so:libm.so.6 so:libstdc++.so.6",
    "p": "so-ver:libicudata.so.78=78.3-r4 so-ver:libicui18n.so.78=78.3-r4 so-ver:libicuio.so.78=78.3-r4 so-ver:libicuuc.so.78=78.3-r4 so:libicudata.so.78=78 so:libicui18n.so.78=78 so:libicuio.so.78=78 so:libicuuc.so.78=78",
    "sha256": "a77f0ed940ecebf98b81a949850ef9d1014005b36775a54d2f73ab4fb392260d"
  },
  {
    "C": "Q1WieibmAzVU9bov1nZqz2iAcu1h4=",
    "P": "libnghttp2-14",
    "V": "1.70.0-r7",
    "A": "x86_64",
    "S": "119856",
    "D": "so:libc.so.6",
    "p": "so-ver:libnghttp2.so.14=1.70.0-r7 so:libnghttp2.so.14=14",
    "sha256": "27c4a41f4c11a6efd6b1eb63f4c59b16233a98fb00bde1c5d16c97735fdebbc7"
  },
  {
    "C": "Q1arwi4n4L3VZ3S8YJ6P4WwY/7JjY=",
    "P": "openssl-4.0-libssl",
    "V": "4.0.3-r8",
    "A": "x86_64",
    "S": "575950",
    "D": "so:libc.so.6 so:libcrypto.so.4",
    "p": "so-ver:libssl.so.4=4.0.3-r8 so:libssl.so.4=4",
    "sha256": "47d1e6276be28279a15e45882ce4262330ef7a80d8f0294b89ba47330fc01c7b"
  },
  {
    "C": "Q1i9+U3koHHdm144haQW6gnhpAF3E=",
    "P": "libuv",
    "V": "1.53.0-r0",
    "A": "x86_64",
    "S": "136308",
    "D": "so:libc.so.6",
    "p": "so-ver:libuv.so.1=1.53.0-r0 so:libuv.so.1=1",
    "sha256": "9432226dda75384b6b75271e67da552ca31d3f8731e9312caaf18743e9127624"
  },
  {
    "C": "Q1Ub6dKp3Ta9ickOJCrZu6zbJa70s=",
    "P": "zlib",
    "V": "1.3.2.1_rc20260921-r1",
    "A": "x86_64",
    "S": "74708",
    "D": "merged-lib so:libc.so.6 wolfi-baselayout",
    "p": "so-ver:libz.so.1=1.3.2.1_rc20260921-r1 so:libz.so.1=1",
    "sha256": "592548698b1563e726709408dc9fc183c595bc5dc463ee6913e9202029952803"
  },
  {
    "C": "Q1NE/aAi9Cgxgxi5QVMjgxoYCmlpc=",
    "P": "nodejs-26",
    "V": "26.12.1-r2",
    "A": "x86_64",
    "S": "33500651",
    "D": "so:ld-linux-x86-64.so.2 so:libbrotlidec.so.1 so:libbrotlienc.so.1 so:libc.so.6 so:libcares.so.2 so:libcrypto.so.4 so:libgcc_s.so.1 so:libicui18n.so.78 so:libicuuc.so.78 so:libm.so.6 so:libnghttp2.so.14 so:libssl.so.4 so:libstdc++.so.6 so:libuv.so.1 so:libz.so.1",
    "p": "cmd:node=26.12.1-r2 nodejs=26.12.1-r2",
    "sha256": "96877171c119620b2bd44afb385b88b6f04a83a2556223b2b9ffa7d949092cb0"
  }
]
''')


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def download(url, path, expected=None):
    if not (expected and path.exists() and sha256(path) == expected):
        temporary = path.with_suffix(path.suffix + ".part")
        subprocess.run(["curl", "--fail", "--location", "--silent", "--show-error",
                        "--retry", "3", url, "--output", str(temporary)], check=True)
        if expected and sha256(temporary) != expected:
            raise RuntimeError(f"SHA256 mismatch: {url}")
        temporary.replace(path)


def index_records(path):
    with tarfile.open(path) as archive:
        data = archive.extractfile("APKINDEX").read().decode()
    return [dict(line.split(":", 1) for line in block.splitlines() if ":" in line)
            for block in data.split("\n\n")]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Empty output directory outside this Git checkout")
    args = parser.parse_args()
    out = args.output.resolve()
    if out == Path(__file__).resolve().parent or Path(__file__).resolve().parent in out.parents:
        parser.error("Use an output directory outside this checkout; APKs must not be committed")
    out.mkdir(parents=True, exist_ok=True)
    download(BASE + "/x86_64/APKINDEX.tar.gz", out / "APKINDEX.tar.gz")
    download(BASE + "/wolfi-signing.rsa.pub", out / "wolfi-signing.rsa.pub", KEY_SHA256)
    records = index_records(out / "APKINDEX.tar.gz")
    for p in PACKAGES:
        matches = [x for x in records if (x.get("P"), x.get("V"), x.get("A")) ==
                   (p["P"], p["V"], "x86_64")]
        if len(matches) != 1 or any(matches[0].get(k, "") != p.get(k, "") for k in ("C", "S", "D", "p")):
            raise RuntimeError(f"Pinned APKINDEX entry missing/changed: {p['P']}={p['V']}; no substitution")
        filename = p["P"] + "-" + p["V"] + ".apk"
        target = out / filename
        download(BASE + "/x86_64/" + filename, target, p["sha256"])
        if target.stat().st_size != int(p["S"]):
            raise RuntimeError(f"Size mismatch: {filename}")
        with tarfile.open(target) as archive:
            metadata = {}
            for line in archive.extractfile(".PKGINFO").read().decode().splitlines():
                if " = " in line:
                    key, value = line.split(" = ", 1)
                    metadata.setdefault(key, []).append(value)
            assert metadata["pkgname"] == [p["P"]], filename
            assert metadata["pkgver"] == [p["V"]], filename
            assert metadata["arch"] == ["x86_64"], filename
            assert set(metadata.get("depend", [])) == set(p.get("D", "").split()), filename
            assert set(metadata.get("provides", [])) == set(p.get("p", "").split()), filename
        print(filename, flush=True)
    files = [out / (p["P"] + "-" + p["V"] + ".apk") for p in PACKAGES]
    files += [out / "APKINDEX.tar.gz", out / "wolfi-signing.rsa.pub"]
    (out / "SHA256SUMS.txt").write_text("".join(f"{sha256(p)}  {p.name}\n" for p in sorted(files)))
    command = ["docker", "run", "--rm", "--network", "none", "--platform", "linux/amd64",
               "-v", f"{out}:/work:ro", IMAGE, "sh", "-c",
               "apk --repositories-file /dev/null --keys-dir /work verify /work/APKINDEX.tar.gz /work/*.apk"]
    try:
        result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        report = result.stdout
        code = result.returncode
    except OSError as error:
        report, code = f"Signature verification NOT RUN: {error}\n", 2
    (out / "signature-verification.txt").write_text(report)
    print(report)
    if code:
        raise SystemExit(2)  # Preserve evidence; never bypass trust or install untrusted APKs.


if __name__ == "__main__":
    main()
