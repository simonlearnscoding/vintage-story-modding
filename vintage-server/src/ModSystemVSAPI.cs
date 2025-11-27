using Vintagestory.API.Common;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using Vintagestory.API.Server;

public class PlayerEvents : ModSystem
{
    private ICoreServerAPI sapi;
    private static readonly HttpClient httpClient = new HttpClient();

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
            playerName = player.PlayerName,
            uid = player.PlayerUID,
            joinedAt = System.DateTime.UtcNow
        };

        string json = JsonSerializer.Serialize(payload);
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        string url = "http://fast-api:8080/join";
        HttpResponseMessage resp = await httpClient.PostAsync(url, content);

    }
    private async System.Threading.Tasks.Task SendLeaveToWebhook(IServerPlayer player)
    {
        var payload = new
        {
            uid = player.PlayerUID,
            disconnectedAt = System.DateTime.UtcNow
        };

        string json = JsonSerializer.Serialize(payload);
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        string url = "http://fast-api:8080/disconnect";
        HttpResponseMessage resp = await httpClient.PostAsync(url, content);

    }
}
    
