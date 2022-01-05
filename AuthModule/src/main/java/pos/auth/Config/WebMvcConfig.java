package pos.auth.Config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/sample/*")
                .allowedMethods("*")
                .allowedHeaders("*")
                .allowedOrigins("http://localhost")
                .allowCredentials(true)
                .maxAge(-1);
    }
}