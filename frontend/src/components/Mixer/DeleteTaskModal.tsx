/* eslint-disable @typescript-eslint/ban-types */
import * as React from 'react';
import { Button, Modal } from 'react-bootstrap';

interface Props {
  isDeleting: boolean;
  show: boolean;
  submit: () => Promise<void>;
  hide: () => void;
}

/**
 * Component for the delete dynamic mix modal.
 */
class DeleteTaskModal extends React.Component<Props, {}> {
  constructor(props: Props) {
    super(props);
  }

  submit = async (): Promise<void> => {
    await this.props.submit();
    this.props.hide();
  };

  render(): JSX.Element | null {
    const { isDeleting } = this.props;
    return (
      <Modal show={this.props.show} onHide={!isDeleting ? this.props.hide : undefined}>
        <Modal.Header closeButton>
          <Modal.Title>Confirmar remoção</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div>Tem certeza de que deseja remover esta mix?</div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="danger" disabled={this.props.isDeleting} onClick={this.submit}>
            Remover
          </Button>
        </Modal.Footer>
      </Modal>
    );
  }
}

export default DeleteTaskModal;
