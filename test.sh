#/bin/bash
mkdir -p /tmp/test/subfolder
cd /tmp/test
for i in {000..1000}
do
    echo hello > "File${i}.txt"
done
nemo /tmp/test
