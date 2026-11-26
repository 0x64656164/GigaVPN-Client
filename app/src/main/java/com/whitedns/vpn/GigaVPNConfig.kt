package com.whitedns.vpn

import android.content.Context
import org.json.JSONObject
import java.io.IOException

/**
 * GigaVPN client configuration.
 *
 * The single source of truth is `assets/config/app_config.json` in the repository root.
 * Gradle copies it into Android assets before every mergeAssets task, so changing one
 * JSON file is enough to point all builds at another Marzban Control Plane.
 */
internal data class GigaVPNConfig(val baseSubscriptionUrl: String) {
    companion object {
        private const val CONFIG_ASSET = "config/app_config.json"

        fun load(context: Context): GigaVPNConfig {
            val raw = context.assets.open(CONFIG_ASSET).bufferedReader().use { it.readText() }
            val base = JSONObject(raw).optString("baseSubscriptionUrl", "").trim()
            if (!base.startsWith("https://")) {
                throw IOException("baseSubscriptionUrl must be an HTTPS URL")
            }
            return GigaVPNConfig(base.trimEnd('/') + "/")
        }
    }

    /** Builds the subscription URL consumed by the existing profile resolver. */
    fun subscriptionUrl(token: String): String = baseSubscriptionUrl + token
}
