import { VaDataTable } from 'vuestic-ui/web-components'
import VaIcon from './components/va-icon'
import iconsConfig from './icons-config/icons-config'

export default {
  icons: iconsConfig,
  breakpoint: {
    enabled: true,
    bodyClass: true,
    thresholds: {
      xs: 0,
      sm: 320,
      md: 640,
      lg: 1024,
      xl: 1440,
    },
  },
  components: {
    VaIcon,
    VaModal: {
      zIndex: 100,
      fixedLayout: true,
    },
    VaInput: {
      color: 'textPrimary'
    },
    VaDateInput: {
      color: 'textPrimary'
    },
    VaCounter: {
      color: 'textPrimary'
    },
    VaSelect: {
      color: 'textPrimary'
    },
    VaFileUpload: {
      color: 'textPrimary'
    },
    VaTextarea: {
      color: 'textPrimary'
    }
  }
}
