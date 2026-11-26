package com.whitedns.vpn

internal object EngineRuntimeYaml {
    fun build(endpoint: SocksEndpoint): String {
        require(endpoint.host == "127.0.0.1" && endpoint.port in 1..65535)
        return """
            proxies:
              - name: GigaVPN Engine
                type: socks5
                server: 127.0.0.1
                port: ${endpoint.port}
                udp: false
            proxy-groups:
              - name: GigaVPN Proxy
                type: select
                proxies:
                  - GigaVPN Engine
              - name: GigaVPN Auto
                type: select
                proxies:
                  - GigaVPN Engine
            rules:
              - NETWORK,UDP,REJECT
              - MATCH,GigaVPN Proxy
        """.trimIndent() + "\n"
    }
}
