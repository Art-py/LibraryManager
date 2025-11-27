#!/bin/bash

echo "Create directory for config..."
mkdir -p /usr/local/etc/redis

echo "Create main config redis..."
cat > /usr/local/etc/redis/redis.conf << EOF
bind 0.0.0.0
appendonly ${REDIS_APPENDONLY}
appendfsync ${REDIS_APPENDFSYNC}
databases ${REDIS_DATABASES}
maxmemory ${REDIS_MAXMEMORY}
EOF

echo "Create ACL file for users..."
cat > /usr/local/etc/redis/users.acl << EOF
user default on >${REDIS_MAIN_USER_PASSWORD} ~* +@all
user ${REDIS_USER} on >${REDIS_USER_PASSWORD} ~* +@all
EOF

echo "Run redis..."
exec redis-server /usr/local/etc/redis/redis.conf --aclfile /usr/local/etc/redis/users.acl