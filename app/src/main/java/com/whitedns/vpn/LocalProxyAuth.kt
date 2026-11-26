package com.whitedns.vpn

import java.net.HttpURLConnection
import java.util.Base64

/**
 * Authentication for the app's local Mihomo mixed proxy.
 *
 * GigaVPN uses the same generated credentials for LAN clients and for its own
 * in-process probes. There is no unauthenticated loopback bypass, so another
 * app on the device cannot silently use the proxy.
 */
internal object LocalProxyAuth {
    @Volatile
    private var proxyAuthorization: String? = null

    fun configure(settings: LanSharingSettings) {
        proxyAuthorization = authorizationHeader(settings)
    }

    fun clear() {
        proxyAuthorization = null
    }

    fun apply(connection: HttpURLConnection) {
        proxyAuthorization?.let { connection.setRequestProperty("Proxy-Authorization", it) }
    }

    /**
     * Pure encoding helper, kept separate from [apply] so it can be verified in
     * JVM tests (the JDK hides Auth headers from [HttpURLConnection.getRequestProperty]).
     */
    internal fun authorizationHeader(settings: LanSharingSettings): String? =
        credential(settings)?.let { "Basic ${encode(it)}" }

    internal fun credential(settings: LanSharingSettings): String? =
        settings.password.takeIf(String::isNotBlank)
            ?.let { "${settings.username}:$it" }

    private fun encode(value: String): String =
        Base64.getEncoder().encodeToString(value.toByteArray(Charsets.UTF_8))
}
