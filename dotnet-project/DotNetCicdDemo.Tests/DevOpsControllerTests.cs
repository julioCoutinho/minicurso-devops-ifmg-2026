using DotNetCicdDemo.Api.Controllers;
using Microsoft.AspNetCore.Mvc;
using Xunit;

namespace DotNetCicdDemo.Tests;

public class DevOpsControllerTests
{
    private readonly DevOpsController _controller;

    public DevOpsControllerTests()
    {
        _controller = new DevOpsController();
    }

    [Fact]
    public void Get_ReturnsOkWithWelcomeMessage()
    {
        // Act
        var result = _controller.Get();

        // Assert
        var okResult = Assert.IsType<OkObjectResult>(result);
        dynamic data = okResult.Value;
        Assert.Equal("Welcome to DevOps Demo API (.NET)", data.Message);
    }

    [Fact]
    public void Health_ReturnsOkWithHealthyStatus()
    {
        // Act
        var result = _controller.Health();

        // Assert
        var okResult = Assert.IsType<OkObjectResult>(result);
        dynamic data = okResult.Value;
        Assert.Equal("Healthy", data.Status);
    }

    [Theory]
    [InlineData(5, 5, 10)]
    [InlineData(-1, 1, 0)]
    [InlineData(0, 0, 0)]
    public void Sum_ReturnsCorrectResult(int a, int b, int expected)
    {
        // Act
        var result = _controller.Sum(a, b);

        // Assert
        var okResult = Assert.IsType<OkObjectResult>(result);
        dynamic data = okResult.Value;
        Assert.Equal(expected, data.Result);
    }
}
