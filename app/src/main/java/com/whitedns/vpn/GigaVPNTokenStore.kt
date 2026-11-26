package com.whitedns.vpn

import android.content.Context

/**
 * Stores the single GigaVPN access token. The app has no profile list: this token
 * is the only credential needed to activate the built-in GigaVPN Private route.
 */
class GigaVPNTokenStore(context: Context) {
    private val prefs = context.applicationContext.getSharedPreferences(
        PREFERENCES_NAME,
        Context.MODE_PRIVATE,
    )

    fun read(): String? = prefs.getString(KEY_TOKEN, null)?.takeIf(String::isNotBlank)

    fun hasToken(): Boolean = read() != null

    fun save(token: String) {
        prefs.edit().putString(KEY_TOKEN, token.trim()).apply()
    }

    fun clear() {
        prefs.edit().remove(KEY_TOKEN).apply()
    }

    private companion object {
        const val PREFERENCES_NAME = "gigavpn_access_token"
        const val KEY_TOKEN = "token"
    }
}
