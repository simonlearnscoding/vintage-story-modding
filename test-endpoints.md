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
    "LastKnownPlayername": "Rasquotcho",
    "LastJoinDate": "11/25/2025 22:00"
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

## Additional Test Data

### Create Multiple Players
```bash
# Player 2
curl -X POST "http://localhost:8000/players/join" \
  -H "Content-Type: application/json" \
  -d '{
    "PlayerUID": "player_002",
    "RoleCode": "admin",
    "PermaPrivileges": ["kick", "ban"],
    "DeniedPrivileges": [],
    "PlayerGroupMemberShips": {"admin": true},
    "AllowInvite": true,
    "LastKnownPlayername": "AdminUser",
    "CustomPlayerData": {"level": 50, "rank": "admin"},
    "ExtraLandClaimAllowance": 10,
    "ExtraLandClaimAreas": 5,
    "FirstJoinDate": "11/26/2025 08:00",
    "LastJoinDate": "11/27/2025 09:00",
    "LastCharacterSelectionDate": "11/27/2025 09:05"
  }'

# Player 3
curl -X POST "http://localhost:8000/players/join" \
  -H "Content-Type: application/json" \
  -d '{
    "PlayerUID": "player_003",
    "RoleCode": "moderator",
    "PermaPrivileges": ["kick"],
    "DeniedPrivileges": ["ban"],
    "PlayerGroupMemberShips": {"mods": true},
    "AllowInvite": true,
    "LastKnownPlayername": "ModUser",
    "CustomPlayerData": {"level": 30, "rank": "moderator"},
    "ExtraLandClaimAllowance": 5,
    "ExtraLandClaimAreas": 2,
    "FirstJoinDate": "11/25/2025 15:00",
    "LastJoinDate": "11/27/2025 11:00",
    "LastCharacterSelectionDate": "11/27/2025 11:10"
  }'

# Player 4
curl -X POST "http://localhost:8000/players/join" \
  -H "Content-Type: application/json" \
  -d '{
    "PlayerUID": "player_004",
    "RoleCode": "vip",
    "PermaPrivileges": [],
    "DeniedPrivileges": [],
    "PlayerGroupMemberShips": {"vip": true},
    "AllowInvite": false,
    "LastKnownPlayername": "VIPPlayer",
    "CustomPlayerData": {"level": 25, "rank": "vip"},
    "ExtraLandClaimAllowance": 3,
    "ExtraLandClaimAreas": 1,
    "FirstJoinDate": "11/24/2025 20:00",
    "LastJoinDate": "11/27/2025 14:00",
    "LastCharacterSelectionDate": "11/27/2025 14:15"
  }'
```

### Simulate Multiple Sessions for Same Player
```bash
# Player 2 joins again (new session)
curl -X POST "http://localhost:8000/players/join" \
  -H "Content-Type: application/json" \
  -d '{
    "PlayerUID": "player_002",
    "RoleCode": "admin",
    "PermaPrivileges": ["kick", "ban"],
    "DeniedPrivileges": [],
    "PlayerGroupMemberShips": {"admin": true},
    "AllowInvite": true,
    "LastKnownPlayername": "AdminUser",
    "CustomPlayerData": {"level": 51, "rank": "admin"},
    "ExtraLandClaimAllowance": 10,
    "ExtraLandClaimAreas": 5,
    "FirstJoinDate": "11/26/2025 08:00",
    "LastJoinDate": "11/27/2025 16:00",
    "LastCharacterSelectionDate": "11/27/2025 16:05"
  }'
```

### Leave Some Players
```bash
# Player 3 leaves
curl -X POST "http://localhost:8000/players/leave" \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "player_003",
    "leftAt": "11/27/2025 13:30"
  }'

# Player 4 leaves
curl -X POST "http://localhost:8000/players/leave" \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "player_004",
    "leftAt": "11/27/2025 17:45"
  }'

# Player 2 leaves first session
curl -X POST "http://localhost:8000/players/leave" \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "player_002",
    "leftAt": "11/27/2025 15:30"
  }'
```

### Test Data Verification
```bash
# Check all players
curl -X GET "http://localhost:8000/players/"

# Check all logs (should show names now)
curl -X GET "http://localhost:8000/players/logs"

# Check specific player logs
curl -X GET "http://localhost:8000/players/player_002/logs"
curl -X GET "http://localhost:8000/players/player_003/logs"
curl -X GET "http://localhost:8000/players/player_004/logs"
```

### Stress Test - Create Many Players
```bash
# Create 10 test players in a loop (bash script)
for i in {5..14}; do
  curl -X POST "http://localhost:8000/players/join" \
    -H "Content-Type: application/json" \
    -d "{
      \"PlayerUID\": \"stress_test_$i\",
      \"RoleCode\": \"player\",
      \"PermaPrivileges\": [],
      \"DeniedPrivileges\": [],
      \"PlayerGroupMemberShips\": {},
      \"AllowInvite\": true,
      \"LastKnownPlayername\": \"StressTest$i\",
      \"CustomPlayerData\": {},
      \"ExtraLandClaimAllowance\": 0,
      \"ExtraLandClaimAreas\": 0,
      \"FirstJoinDate\": \"11/27/2025 $(printf '%02d' $((i%24))):00\",
      \"LastJoinDate\": \"11/27/2025 $(printf '%02d' $((i%24))):00\",
      \"LastCharacterSelectionDate\": \"11/27/2025 $(printf '%02d' $((i%24))):05\"
    }"
  echo "Created stress_test_$i"
done
```