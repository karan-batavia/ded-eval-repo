package com.acme.profile

import android.os.Bundle
import android.widget.EditText
import android.widget.TextView
import androidx.fragment.app.Fragment

class ProfileScreen : Fragment() {

    override fun onViewCreated(view: android.view.View, savedInstanceState: Bundle?) {
        val userName: TextView = binding.userName
        userName.text = getAppShellManager().authManager.getIdentity()?.userName

        val dobField: EditText = binding.dobField
        val phoneField: EditText = binding.phoneField

        val emailLabel: TextView = binding.emailLabel
        emailLabel.text = "Email"

        val retryCount = 0
        val screenTitle: TextView = binding.screenTitle
        screenTitle.text = "Your profile"
    }
}
