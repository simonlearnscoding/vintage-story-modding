using System.Text;
using System.Text.Json;
using Vintagestory.API.Common;
using Vintagestory.API.Common.Entities;
using Vintagestory.API.Server;

namespace VSAPI;

public class PlayerEvents : ModSystem
{
#pragma warning disable CS8618 // Non-nullable field must contain a non-null value when exiting constructor. Consider adding the 'required' modifier or declaring as nullable.
    private ICoreServerAPI _sapi;
#pragma warning restore CS8618 // Non-nullable field must contain a non-null value when exiting constructor. Consider adding the 'required' modifier or declaring as nullable.
    
    private static readonly HttpClient HttpClient = new HttpClient();
    private static readonly int Maxdeaths = 20;
    private const bool Prod = false;
    // API-URL-Placeholder - Later build something to get the prod state somewhere
    private readonly string _apiBaseUrl = Prod ? "https://vsm.pasquotcho.com/api" : "http://host.docker.internal:8000";
    
    public override void StartServerSide(ICoreServerAPI api)
    {
        _sapi = api;
        api.Event.PlayerJoin += OnPlayerJoin;
        api.Event.PlayerLeave += OnPlayerLeave;
        api.Event.PlayerDisconnect += OnPlayerLeave;
        api.Event.PlayerDeath += OnPlayerDeath;
    }

    private void OnPlayerDeath(IServerPlayer player, DamageSource damageSource)
    {
        _sapi.Logger.Notification($"{player.PlayerName} died because of {damageSource}");
        _sapi.Logger.Notification($"Deaths: {player.WorldData.Deaths}\nRemaining: {Maxdeaths - player.WorldData.Deaths}");
        SendDeath(player, damageSource);
    }

    private void OnPlayerJoin(IServerPlayer player)
    {
        _sapi.Logger.Notification($"[Join] {player.PlayerUID} hat den Server betreten.");
        _sapi.Logger.Notification($"Deaths: {player.WorldData.Deaths}\nRemaining: {Maxdeaths - player.WorldData.Deaths}");
        SendJoin(player);
    }

    private void OnPlayerLeave(IServerPlayer player)
    {
        _sapi.Logger.Notification($"[Leave] {player.PlayerUID} hat den Server verlassen.");
        SendLeave(player);
    }
    
    private void SendJoin(IServerPlayer player)
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
        string url = "/players/join";
        string eventName = "join";
        _ = SendWebhook(url, content, eventName);
    }
    
    private void SendLeave(IServerPlayer player)
    {
        var payload = new
        {
            // ReSharper disable once RedundantAnonymousTypePropertyName
            PlayerUID = player.PlayerUID,
            leftAt = DateTime.Now.ToString("MM/dd/yyyy HH:mm")
        };
        string json = JsonSerializer.Serialize(payload);
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        string url = "/players/leave";
        string eventName = "leave";
        _ = SendWebhook(url, content, eventName);
    }
    private void SendDeath(IServerPlayer player, DamageSource damageSource)
    {
        Entity causeEntity = damageSource.GetCauseEntity();
        string causeEntityName = causeEntity == null
            ? damageSource.Type.ToString()
            : causeEntity.GetName();
        
        var payload = new
        {
            // ReSharper disable once RedundantAnonymousTypePropertyName
            PlayerUID = player.PlayerUID,
            damageSource = causeEntityName,
            deathTime = DateTime.Now.ToString("MM/dd/yyyy HH:mm")
        };
        string json = JsonSerializer.Serialize(payload);
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        string url = "/players/death";
        string eventName = "death";
        _ = SendWebhook(url, content, eventName);
    }
    
    private async Task SendWebhook(string url, StringContent content, string eventName)
    {
        string wholeUrl = $"{_apiBaseUrl}{url}";
        try 
        {
            HttpResponseMessage resp = await HttpClient.PostAsync(wholeUrl, content);
            if (!resp.IsSuccessStatusCode)
            {
                _sapi.Logger.Error($"Failed to send {eventName} event: {resp.StatusCode}");
            }
        }
        catch (Exception ex)
        {
            _sapi.Logger.Error($"Error sending {eventName} event: {ex.Message}");
        }
    }
}