using System.Text;
using System.Text.Json;
using Vintagestory.API.Common;
using Vintagestory.API.Server;

namespace VSAPI;

public class PlayerEvents : ModSystem
{
#pragma warning disable CS8618 // Non-nullable field must contain a non-null value when exiting constructor. Consider adding the 'required' modifier or declaring as nullable.
    private ICoreServerAPI _sapi;
#pragma warning restore CS8618 // Non-nullable field must contain a non-null value when exiting constructor. Consider adding the 'required' modifier or declaring as nullable.
    
    private static readonly HttpClient HttpClient = new HttpClient();

    private const bool Prod = false;
    // API-URL-Placeholder - Later build something to get the prod state somewhere
    private readonly string _apiBaseUrl = Prod ? "https://vsm.pasquotcho.com/api" : "http://host.docker.internal:8000";
        
    public override void StartServerSide(ICoreServerAPI api)
    {
        _sapi = api;
        api.Event.PlayerJoin += OnPlayerJoin;
        api.Event.PlayerLeave += OnPlayerLeave;
        api.Event.PlayerDisconnect += OnPlayerLeave;
    }

    private void OnPlayerJoin(IServerPlayer player)
    {
        _sapi.Logger.Notification($"[Join] {player.PlayerName} hat den Server betreten.");
        _ = SendJoinToWebhook(player);
    }

    private void OnPlayerLeave(IServerPlayer player)
    {
        _sapi.Logger.Notification($"[Leave] {player.PlayerName} hat den Server verlassen.");
        _ = SendLeaveToWebhook(player);
    }
    
    private async Task SendJoinToWebhook(IServerPlayer player)
    {
        var payload = new
        {
            // ReSharper disable once RedundantAnonymousTypePropertyName
            PlayerUID = player.PlayerUID,
            LastKnownPlayername = player.PlayerName,
            LastJoinDate = DateTime.Now.ToString("MM/dd/yyyy HH:mm")
        };

        string json = JsonSerializer.Serialize(payload);
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        string url = $"{_apiBaseUrl}/players/join";
        
        try 
        {
            HttpResponseMessage resp = await HttpClient.PostAsync(url, content);
            if (!resp.IsSuccessStatusCode)
            {
                _sapi.Logger.Error($"Failed to send join event: {resp.StatusCode}");
            }
        }
        catch (Exception ex)
        {
            _sapi.Logger.Error($"Error sending join event: {ex.Message}");
        }
    }
    
    private async Task SendLeaveToWebhook(IServerPlayer player)
    {
        var payload = new
        {
            uid = player.PlayerUID,
            leftAt = DateTime.Now.ToString("MM/dd/yyyy HH:mm")
        };

        string json = JsonSerializer.Serialize(payload);
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        string url = $"{_apiBaseUrl}/players/leave";
        
        try 
        {
            HttpResponseMessage resp = await HttpClient.PostAsync(url, content);
            if (!resp.IsSuccessStatusCode)
            {
                _sapi.Logger.Error($"Failed to send leave event: {resp.StatusCode}");
            }
        }
        catch (Exception ex)
        {
            _sapi.Logger.Error($"Error sending leave event: {ex.Message}");
        }
    }
}