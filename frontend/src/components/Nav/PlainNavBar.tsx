import * as React from 'react';
import { Container, Nav, Navbar } from 'react-bootstrap';
import { withRouter } from 'react-router';

/**
 * Plain navigation bar.
 */
const PlainNavBar = (): JSX.Element => {
  return (
    <Navbar bg="light" variant="light" expand="lg">
      <Container>
        <Navbar.Brand href="/">Help Musician</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="/">Inicio</Nav.Link>
            <Nav.Link href="/lista/">Minha Lista</Nav.Link>
            <Nav.Link href="/drumkit/">Drums Kit</Nav.Link>
            <Nav.Link href="/worship-pads/">Worship Pads</Nav.Link>
          </Nav>
          <Nav className="ml-auto">
            <Nav.Link href="/logout/">Logout</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default withRouter(PlainNavBar);
