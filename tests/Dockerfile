FROM hbpmip/java-base-build:3.5.0-jdk-8-9 as build-java-env

COPY pom.xml /project/pom.xml
# Fill the cache for jar dependencies, to allow code changes reusing previously downloaded jars
RUN cp /usr/share/maven/ref/settings-docker.xml /root/.m2/settings.xml \
    && mvn dependency:resolve

COPY src/ /project/src

# Repeating copy of the settings works better. I dunno why.
RUN cp /usr/share/maven/ref/settings-docker.xml /root/.m2/settings.xml \
    && mvn package assembly:single site

FROM hbpmip/java-mip:0.5.1

ENV JAVA_CLASSPATH=/usr/share/jars/java-mip.jar
ENV JAVA_MAINCLASS=eu.humanbrainproject.mip.algorithms.Main

COPY --from=build-java-env /project/target/java-mip-jar-with-dependencies.jar /usr/share/jars/java-mip.jar
COPY --from=build-java-env /project/target/site/ /var/www/html/
COPY src/ /src/

RUN chown -R compute:compute /src/ \
    && chown -R root:www-data /var/www/html/
