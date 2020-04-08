#!/bin/sh



bert-serving-start -num_worker 1 -max_seq_len 128  -model_dir /model -http_port 8001
