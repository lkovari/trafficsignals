plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.compose) apply false
}

tasks.register<Exec>("unifySignArt") {
    workingDir = rootDir
    commandLine(
        "bash",
        "-lc",
        """
        set -euo pipefail
        cd "$rootDir"
        if [ ! -x tools/sign-art/.venv/bin/python3 ]; then
          python3 -m venv tools/sign-art/.venv
          tools/sign-art/.venv/bin/pip install pillow numpy
        fi
        tools/sign-art/.venv/bin/python3 tools/sign-art/unify_palette.py
        tools/sign-art/.venv/bin/python3 tools/sign-art/render_category_icons.py
        tools/sign-art/.venv/bin/python3 tools/sign-art/render_launcher.py
        echo JPG ${'$'}(find app/src/main/res/drawable-xxhdpi \( -iname '*.jpg' -o -iname '*.jpeg' \) | wc -l)
        echo PNG ${'$'}(find app/src/main/res/drawable-xxhdpi -iname '*.png' | wc -l)
        """.trimIndent()
    )
}
