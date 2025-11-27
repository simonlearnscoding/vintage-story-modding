# API Test Endpoints

## Base URL
```
http://localhost:8000
```

## Player Management

### Create Player
```bash
curl -X POST "http://localhost:8000/players/" \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "test_player_123",
    "name": "TestPlayer"
  }'
```

### Get Specific Player
```bash
curl -X GET "http://localhost:8000/players/test_player_123"
```

### Get All Players
```bash
curl -X GET "http://localhost:8000/players/"
```

## Player Join/Leave

### Player Join
```bash
curl -X POST "http://localhost:8000/players/join" \
  -H "Content-Type: application/json" \
  -d '{
    "PlayerUID": "AYnENYK0ecf2f2vPgDlXgP3U",
    "RoleCode": "suplayer",
    "PermaPrivileges": [],
    "DeniedPrivileges": [],
    "PlayerGroupMemberShips": {},
    "AllowInvite": true,
    "LastKnownPlayername": "GGGGGGG",
    "CustomPlayerData": {},
    "ExtraLandClaimAllowance": 0,
    "ExtraLandClaimAreas": 0,
    "FirstJoinDate": "11/25/2025 21:10",
    "LastJoinDate": "11/25/2025 21:41",
    "LastCharacterSelectionDate": "11/25/2025 21:13"
  }'
```

### Player Leave
```bash
curl -X POST "http://localhost:8000/players/leave" \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "AYnENYK0ecf2f2vPgDlXgP3U",
    "leftAt": "11/25/2025 22:00"
  }'
```

## Player Logs

### Get Logs for Specific Player
```bash
curl -X GET "http://localhost:8000/players/AYnENYK0ecf2f2vPgDlXgP3U/logs"
```

### Get All Player Logs
```bash
curl -X GET "http://localhost:8000/players/logs"
```

## Health Check

### Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

## Test Workflow Example

1. **Join a player:**
   ```bash
   curl -X POST "http://localhost:8000/players/join" \
     -H "Content-Type: application/json" \
     -d '{
       "PlayerUID": "test_user_001",
       "RoleCode": "player",
       "PermaPrivileges": [],
       "DeniedPrivileges": [],
       "PlayerGroupMemberShips": {},
       "AllowInvite": true,
       "LastKnownPlayername": "TestUser",
       "CustomPlayerData": {},
       "ExtraLandClaimAllowance": 0,
       "ExtraLandClaimAreas": 0,
       "FirstJoinDate": "11/27/2025 10:00",
       "LastJoinDate": "11/27/2025 10:00",
       "LastCharacterSelectionDate": "11/27/2025 10:05"
     }'
   ```

2. **Check logs (should show join with no leave time):**
   ```bash
   curl -X GET "http://localhost:8000/players/test_user_001/logs"
   ```

3. **Leave the player:**
   ```bash
   curl -X POST "http://localhost:8000/players/leave" \
     -H "Content-Type: application/json" \
     -d '{
       "uid": "test_user_001",
       "leftAt": "11/27/2025 12:00"
     }'
   ```

4. **Check logs again (should show join with leave time):**
   ```bash
   curl -X GET "http://localhost:8000/players/test_user_001/logs"
   ```