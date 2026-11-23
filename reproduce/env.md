# 环境搭建逐条记录

目的：换机器时能照着复现，不用再查。

## 系统

- Ubuntu 22.04（上游唯一官方测试过的系统，Windows / macOS 不支持）
- NVIDIA 驱动：待填
- CUDA：待填

## 依赖

```bash
# git lfs
sudo apt-get install -y git-lfs

# uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 仓库

```bash
git clone --recurse-submodules git@github.com:Physical-Intelligence/openpi.git
cd openpi

# 跳过 LFS 大文件下载，先加速拉依赖
GIT_LFS_SKIP_SMUDGE=1 uv sync
GIT_LFS_SKIP_SMUDGE=1 uv pip install -e .
```

## 权重

- 默认从 `gs://openpi-assets` 拉取；国内网络不通时，记录实际使用的镜像/HuggingFace 路径：待填
- 本地缓存目录：待填

## 校验

- [ ] `uv run python -c "import openpi"` 成功
- [ ] 能加载 π0.5 权重并输出一条动作
- [ ] LIBERO 环境可以起仿真
