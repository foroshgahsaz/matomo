<?php

/**
 * Matomo - free/libre analytics platform
 *
 * @link    https://matomo.org
 * @license https://www.gnu.org/licenses/gpl-3.0.html GPL v3 or later
 */

namespace Piwik\Plugins\PersianLocalization;

use Piwik\Plugin;
use Piwik\Plugins\LanguagesManager\LanguagesManager;

class PersianLocalization extends Plugin
{
    /**
     * @see \Piwik\Plugin::registerEvents
     */
    public function registerEvents()
    {
        return [
            'AssetManager.getStylesheetFiles' => 'getStylesheetFiles',
            'AssetManager.getJavaScriptFiles' => 'getJavaScriptFiles',
            'Template.bodyClass' => 'addBodyClass',
            'Template.bodyTop' => 'onBodyTop',
        ];
    }

    public function getStylesheetFiles(&$stylesheets)
    {
        if (!$this->isPersianInterface()) {
            return;
        }

        $stylesheets[] = 'plugins/PersianLocalization/stylesheets/persian.less';
    }

    public function getJavaScriptFiles(&$jsFiles)
    {
        if (!$this->isPersianInterface()) {
            return;
        }

        $jsFiles[] = 'plugins/PersianLocalization/javascripts/persian.js';
    }

    /**
     * @param string $bodyClass
     * @return string
     */
    public function addBodyClass($bodyClass)
    {
        if (!$this->isPersianInterface()) {
            return $bodyClass;
        }

        return trim($bodyClass . ' matomo-persian matomo-rtl');
    }

    public function onBodyTop()
    {
        if (!$this->isPersianInterface()) {
            return;
        }

        echo '<script>document.documentElement.setAttribute("dir","rtl");</script>';
    }

    private function isPersianInterface(): bool
    {
        return LanguagesManager::getLanguageCodeForCurrentUser() === 'fa';
    }
}
