# NOTES

## The `ping` command is different on each OS

On Windows:
```
ping -n 1 -w 2000 8.8.8.8
```

`-n 1` = send 1 packet
`-w 2000` = wait up to 2000 milliseconds (2 seconds) for a reply

On Linux/macOS:
```
ping -c 1 -W 2 8.8.8.8
```

`-c 1` = send 1 packet
`-W 2` = wait up to 2 seconds

I end up deciding not to add different ping command parsing like from the Linux/macOS to this script.

## `ping_host(host)`

When doing this:
```python
def ping_host(host):
    """
    Pings a single host once.
    Returns latency in ms as a float, or None if the host is unreachable.
    """
    system = platform.system()
    print(f"Pinging {host} on {system}...")
    if system == "Windows":
        command = ["ping", "-n", "1", "-w", "2000", host]
    else:
        command = None

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,     # With PIPE: output is silent in the terminal but accessible via result.stdout.
            text=True
        )
        output = result.stdout
        print(f"Test {host}: {output}")
        return None
    except Exception as e:
        print(f"Error pinging {host}: {e}")
        return None

```

It prints:
```
Pinging github.com on Windows...
Test github.com: 
Pinging github.com [4.237.22.38] with 32 bytes of data:
Reply from 4.237.22.38: bytes=32 time=51ms TTL=113

Ping statistics for 4.237.22.38:
    Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 51ms, Maximum = 51ms, Average = 51ms
```

### Break the output into `lines`

When doing this:
```python
def ping_host(host):
    """
    Pings a single host once.
    Returns latency in ms as a float, or None if the host is unreachable.
    """
    system = platform.system()
    print(f"Pinging {host} on {system}...")
    if system == "Windows":
        command = ["ping", "-n", "1", "-w", "2000", host]
    else:
        command = None

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,     # With PIPE: output is silent in the terminal but accessible via result.stdout.
            text=True
        )
        output = result.stdout

        # Parse latency from ping output
        if system == "Windows":
            # Windows output example: "Average = 14ms"
            for line in output.splitlines():
                print(f"Line: {line}")
                if "Average" in line:
                    parts = line.split("=")
                    print(f"parts: {parts}")

        return None
    except Exception as e:
        print(f"Error pinging {host}: {e}")
        return None
```

It prints:
```
Line: Pinging github.com [4.237.22.38] with 32 bytes of data:
Line: Reply from 4.237.22.38: bytes=32 time=51ms TTL=113
Line: 
Line: Ping statistics for 4.237.22.38:
Line:     Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),
Line: Approximate round trip times in milli-seconds:
Line:     Minimum = 51ms, Maximum = 51ms, Average = 51ms
parts: ['    Minimum ', ' 51ms, Maximum ', ' 51ms, Average ', ' 51ms']
```

And this:
```python
latency_str = parts[-1].strip().replace("ms", "")
```

prints this:
```
latency_str: 51
```

### Why using `subprocess`
`ping` is an external program that lives outside Python. Python cannot run it directly. `subprocess` is the bridge that lets Python launch external programs.

Without `subprocess.PIPE`, the output from `ping` goes straight to your terminal and Python has no way to read it. `subprocess.PIPE` redirects that output into Python's memory, so you can store it in a variable and parse it.

A simple way to think about it:
```
ping command  -->  subprocess.PIPE  -->  result.stdout  -->  your Python code
```

## Add Linux Support

I used GitHub codespace for the Linux ping command and parse related code in the script.

The ping command is not installed by default in many minimal Linux containers, including GitHub Codespaces.

So I ended up installing the `ping` package like this:
```
sudo apt-get update && sudo apt-get install -y inetutils-ping
```

But when I run:
```
ping -c 1 -W 2 8.8.8.8
```

It prints:
```
PING 8.8.8.8 (8.8.8.8): 56 data bytes
--- 8.8.8.8 ping statistics ---
1 packets transmitted, 0 packets received, 100% packet loss
```

That output shows 100% packet loss, which means the ping was blocked. This is common in cloud environments like GitHub Codespaces. 

ICMP (the protocol ping uses) is often blocked by the firewall there.

So I decided to replace ping with a TCP port check i.e. instead of ICMP ping, connect to port 443 (HTTPS) on each host.

So the `ping_host()` method:
- On Linux/macOS inside Codespaces, use the TCP socket method.
- On Windows,I keep the ICMP ping.
