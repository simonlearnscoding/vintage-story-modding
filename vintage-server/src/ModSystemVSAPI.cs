using Vintagestory.API.Common;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using Vintagestory.API.Server;

public class PlayerEvents : ModSystem
{
    private ICoreServerAPI sapi;
    private static readonly HttpClient httpClient = new HttpClient();
    
    // API-URL-Placeholder 
    private readonly string apiBaseUrl = "http://localhost:8000";

    public override void StartServerSide(ICoreServerAPI api)
    {
        sapi = api;
        api.Event.PlayerJoin += OnPlayerJoin;
        api.Event.PlayerLeave += OnPlayerLeave;
        api.Event.PlayerDisconnect += OnPlayerLeave;
    }

    private void OnPlayerJoin(IServerPlayer player)
    {
        sapi.Logger.Notification($"[Join] {player.PlayerName} hat den Server betreten.");
        _ = SendJoinToWebhook(player);
    }

    private void OnPlayerLeave(IServerPlayer player)
    {
        sapi.Logger.Notification($"[Leave] {player.PlayerName} hat den Server verlassen.");
        _ = SendLeaveToWebhook(player);
    }
    
    private async System.Threading.Tasks.Task SendJoinToWebhook(IServerPlayer player)
    {
        var payload = new
        {
            PlayerUID = player.PlayerUID,
            LastKnownPlayername = player.PlayerName,
            LastJoinDate = System.DateTime.UtcNow.ToString("MM/dd/yyyy HH:mm")
        };

        string json = JsonSerializer.Serialize(payload);
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        string url = $"{apiBaseUrl}/players/join";
        
        try 
        {
            HttpResponseMessage resp = await httpClient.PostAsync(url, content);
            if (!resp.IsSuccessStatusCode)
            {
                sapi.Logger.Error($"Failed to send join event: {resp.StatusCode}");
            }
        }
        catch (Exception ex)
        {
            sapi.Logger.Error($"Error sending join event: {ex.Message}");
        }
    }
    
    private async System.Threading.Tasks.Task SendLeaveToWebhook(IServerPlayer player)
    {
        var payload = new
        {
            uid = player.PlayerUID,
            leftAt = System.DateTime.UtcNow.ToString("MM/dd/yyyy HH:mm")
        };

        string json = JsonSerializer.Serialize(payload);
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        string url = $"{apiBaseUrl}/players/leave";
        
        try 
        {
            HttpResponseMessage resp = await httpClient.PostAsync(url, content);
            if (!resp.IsSuccessStatusCode)
            {
                sapi.Logger.Error($"Failed to send leave event: {resp.StatusCode}");
            }
        }
        catch (Exception ex)
        {
            sapi.Logger.Error($"Error sending leave event: {ex.Message}");
        }
    }
}
    
