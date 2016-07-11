import groovyx.net.http.RESTClient
import spock.lang.Specification
import spock.lang.Stepwise


@Stepwise
class BlackbookAPI extends Specification {

    def client = new RESTClient('http://localhost:27222')

    def "GET /trips returns status 200"() {
        when:
          def resp = client.get path: '/trips'

        then:
          resp.status == 200
    }

    def "GET /trips returns text/json content-type"() {
        when:
          def resp = client.get path: '/trips'

        then:
          resp.contentType == 'text/json'

    }

}