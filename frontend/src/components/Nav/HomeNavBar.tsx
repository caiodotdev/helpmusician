import * as React from 'react';
import { Button, Container, Navbar, Nav } from 'react-bootstrap';
import { CloudUpload } from 'react-bootstrap-icons';
import { withRouter, RouteComponentProps } from 'react-router';

interface Props extends RouteComponentProps {
  onUploadClick: () => void;
}

/**
 * Navigation bar with upload button.
 */
const HomeNavBar = (props: Props): JSX.Element => {
  return (
    <Navbar bg="light" variant="light" expand="lg">
      <Container>
        <Navbar.Brand href="/">Help Musician</Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse className="text-right">
          <Nav className="me-auto">
            <Nav.Link href="/">Inicio</Nav.Link>
            <Nav.Link href="/lista/">Minha Lista</Nav.Link>
            <Nav.Link href="/drumkit/">Drums Kit</Nav.Link>
            <Nav.Link href="/worship-pads/">Worship Pads</Nav.Link>
          </Nav>
          <Nav className="ml-auto">
            <Button onClick={props.onUploadClick} variant="success mr-3">
              Upload <CloudUpload />
            </Button>
            <Nav.Link href="/logout/">Logout</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default withRouter(HomeNavBar);
