package blackbook

import groovyx.net.http.RESTClient
import spock.lang.Specification
import spock.lang.Stepwise


@Stepwise
class Server extends Specification {

    def client = new RESTClient('http://localhost:27222')

    def "Server is up"() {
        when:
          def resp = client.get path: '/'

        then:
          resp.status == 200
    }

    def "Root content type is text/html"() {
        when:
          def resp = client.get path: '/'

        then:
          resp.contentType == 'text/html'
    }

}