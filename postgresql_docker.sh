#!/bin/bash

docker run --name postgresql -v pgdata:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres -p "5432:5432" -d postgres