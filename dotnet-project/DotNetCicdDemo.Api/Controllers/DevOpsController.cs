using Microsoft.AspNetCore.Mvc;

namespace DotNetCicdDemo.Api.Controllers;

[ApiController]
[Route("[controller]")]
public class DevOpsController : ControllerBase
{
    [HttpGet]
    public IActionResult Get()
    {
        return Ok(new
        {
            Message = "Welcome to DevOps Demo API (.NET)",
            Timestamp = DateTime.UtcNow,
            Status = "Healthy"
        });
    }

    [HttpGet("health")]
    public IActionResult Health()
    {
        return Ok(new
        {
            Status = "Healthy",
            Version = "1.0.0"
        });
    }

    [HttpGet("sum")]
    public IActionResult Sum(int a, int b)
    {
        return Ok(new { Result = a + b });
    }
}
