#!/usr/bin/env bash
# Vista Leest database backup script
# Cron: 0 0 * * * /bin/bash ~/Projects/vistabieb/backup.sh >> ~/Projects/vistabieb/backups/backup.log 2>&1

set -e

BACKUP_DIR="$(dirname "$0")/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Create backup
pg_dump vistabieb > "$BACKUP_DIR/vistabieb_$TIMESTAMP.sql"
echo "$(date '+%Y-%m-%d %H:%M:%S') — Backup gemaakt: vistabieb_$TIMESTAMP.sql"

# Delete backups older than 7 days
find "$BACKUP_DIR" -name "vistabieb_*.sql" -mtime +7 -delete
echo "$(date '+%Y-%m-%d %H:%M:%S') — Oude backups (>7 dagen) verwijderd"
