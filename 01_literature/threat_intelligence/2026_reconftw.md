[[ PAGE 1 ]]

# Practical Recon Automation with ReconFTW

I have always used automation for bounty hunting or quick tests. Automation allows you to run multiple tools one after another without wasting time manually executing commands. There are always two problems. The first is that you have to choose the right tools, not too many and not too few. Tools need to be developed, and any major change can break the automation. The second problem is that no automation will do all the work for us. Regardless of whether you use a single tool or an entire pipeline, you always end up with output files. These results must be reviewed manually, conclusions drawn, and only then can the next steps be planned (often: additional tools, manual tests, refinement of the scope).

![ReconFTW](reconftw.webp)

Of course, you can put both input and output into AI, as I described in [HexStrike AI on Kali with Roo Code](../../../01/11/hexstrikeai-setup/index.html), but it will be some time before AI can do everything for us at an expert level. At least, that’s my opinion.

The easiest way to automate tasks is in specific cases. That is why tools such as SQLMap are being developed, which automate and accelerate SQL injection attacks. In other words, they help in a given category or type. Another example is automating the entire stage of, for example, reconnaissance. Reconnaissance is the process of gathering basic information and looking for points of entry. This only requires a few tools, and the fun part is analyzing the results and exploring the preliminary information.

[ReconFTW](https://github.com/six2dez/reconftw) is a very cool example of an actively developed tool that collects massive amounts of information about a target, generates several reports from individual tools, and saves them as output files for manual or AI-assisted analysis. Since I have used ReconFTW many times in my work, I decided to describe how to set it up on a virtual machine and how to use it.

If you are a beginner bounty hunter, simply setting up this tool and then using it along with analyzing the results will allow you to learn a few things. If you are already more advanced, it may help you speed up your work. After all, the point is to speed up manual tasks and focus on analyzing the results.

To begin with, download the latest [Debian Net Install](https://www.debian.org/CD/netinst/) and install it using your favorite virtualization program. I use virt-manager.

## Sudo

After installation, switch to root:

```bash
su -
```

Install sudo:

```bash
apt install -y sudo
```

Add user to sudo (example: user):

```bash
adduser user sudo
exit
```

Wyloguj/zaloguj się ponownie i test:

```bash
sudo whoami
```

It should be:

```plaintext
root
```

## Docker installation (official Docker repository)

```bash
sudo apt install -y ca-certificates curl gnupg mc nano

sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/debian/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/debian \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update

sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Enable Docker at system startup:

```bash
sudo systemctl enable --now docker
```

Set up Docker without sudo:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

After `usermod -aG docker $USER`, you may need to log out/log in, and `newgrp docker` works “for this session.”

reconFTW directories in `/opt`

```bash
sudo mkdir -p /opt/reconftw/{reports,lists,tmp}
sudo chown -R $USER:$USER /opt/reconftw
```

- `/opt/reconftw/reports` → scan results
- `/opt/reconftw/tmp` → working catalog

### Download the reconFTW image

```bash
cd /opt/reconftw/
docker pull six2dez/reconftw:main
```

## Wrapper `reconftw`

The wrapper simplifies working with reconFTW running in Docker.

It provides consistent result directories, automatic timestamps, and the ability to update the image without having to remember long `docker run` commands. This gives each scan a predictable structure and makes it easy to archive or analyze later.

Goal:

- Run `reconftw -d target -r`
- The results are stored in `/opt/reconftw/reports/<target_timestamp>/`
- `reconftw -h/--help` displays the original help

### Create a wrapper

```bash
sudo nano /usr/local/bin/reconftw
```

Paste:

```bash
#!/usr/bin/env bash
set -euo pipefail

IMAGE="six2dez/reconftw:main"
BASE="/opt/reconftw/reports"

usage() {
  cat <<'EOF'
Wrapper usage:
  reconftw -d domain.tld [reconFTW options...]
  reconftw -l /opt/reconftw/lists/domains.txt [reconFTW options...]

Wrapper actions:
  reconftw --update      # docker pull the latest image
  reconftw               # no args -> show this help

Original reconFTW help:
  reconftw -h
  reconftw --help
EOF
}

# No args -> wrapper help
if [[ $# -eq 0 ]]; then
  usage
  exit 1
fi

# Wrapper update action
if [[ "${1:-}" == "--update" ]]; then
  docker pull "$IMAGE"
  exit 0
fi

# If user requests help, do NOT create output folders; just run the container help.
for a in "$@"; do
  if [[ "$a" == "-h" || "$a" == "--help" ]]; then
    exec docker run -it --rm "$IMAGE" "$@"
  fi
done

mkdir -p "$BASE"
ts="$(date +%Y%m%d_%H%M%S)"

# Derive a friendly folder name from -d or -l
target="scan"
for ((i=1; i<=$#; i++)); do
  if [[ "${!i}" == "-d" ]]; then
    j=$((i+1))
    target="${!j:-scan}"
    break
  fi
  if [[ "${!i}" == "-l" ]]; then
    j=$((i+1))
    listpath="${!j:-}"
    target="$(basename "${listpath:-list}")"
    target="${target%.*}"
    break
  fi
done

OUT="$BASE/${target}_${ts}"
mkdir -p "$OUT"

echo "[*] Output directory: $OUT"
echo "[*] Docker image:      $IMAGE"
echo

docker run -it --rm \
  -v "$OUT/:/reconftw/Recon/" \
  -v "/opt/reconftw/lists:/opt/reconftw/lists:ro" \
  -v "/opt/reconftw/tmp:/opt/reconftw/tmp" \
  "$IMAGE" "$@"
```

Rights to launch:

```bash
sudo chmod +x /usr/local/bin/reconftw
```

## Use of reconFTW

Original help reconFTW:

```bash
reconftw -h
```

Docker image update:

```bash
reconftw --update
```

Scan of one domain:

```bash
reconftw -d example.com -r
```

Scan of the domain list:

```bash
printf "example.com\nexample.org\n" > /opt/reconftw/lists/domains.txt
reconftw -l /opt/reconftw/lists/domains.txt -r
```

Each launch of reconFTW performs a full reconnaissance phase: subdomain enumeration, analysis of HTTP, TLS, and endpoint services, and basic fuzzing. The tool does not find vulnerabilities on its own, but provides input for further manual analysis.

### Where are the results?

In practice, most of the time is spent in this directory - reviewing reports and selecting interesting artifacts for further manual testing.

Each run creates:

```bash
/opt/reconftw/reports/<target>_<timestamp>/
```

And inside reconFTW usually creates another target folder:

```bash
/opt/reconftw/reports/<target>_<timestamp>/<target>/
```

Packing the results into a single downloadable package:

```bash
cd /opt/reconftw/reports
tar -czf example.com_20260208_123000.tar.gz example.com_20260208_123000/
```

Such an archive can be easily transferred to a host machine, uploaded to a reporting tool, or forwarded for further analysis (e.g., offline or using AI).

## WWW listing of reports

Installing nginx

```bash
sudo apt update
sudo apt install -y nginx
sudo systemctl enable --now nginx
```

Vhost configuration on 1234

```bash
sudo nano /etc/nginx/sites-available/reconftw-reports
```

Paste:

```bash
server {
    listen 1234;
    server_name _;

    root /opt/reconftw/reports;
    index index.html index.htm;

    location / {
        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;

        try_files $uri $uri/ =404;
    }
}
```

Note: autoindex nginx should only be used in a lab or trusted network (host-only / VPN).

Enable configuration:

```bash
sudo ln -s /etc/nginx/sites-available/reconftw-reports /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
```

Test and reload:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

File read permissions for nginx:

```bash
sudo chmod -R o+rX /opt/reconftw/reports
```

### Accessing reports from the host

In your browser:

```bash
http://IP_VM:1234/
```

Automation makes sense when it simplifies workflow, not when it tries to replace thinking. ReconFTW works well as the first stage of work quick reconnaissance, data collection, and setting the direction for further action.

What you do with that data next still depends on experience, context, and manual analysis. And that’s exactly how it should be.

Happy hunting!
