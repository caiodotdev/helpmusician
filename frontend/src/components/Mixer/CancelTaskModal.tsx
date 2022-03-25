/* eslint-disable @typescript-eslint/ban-types */
import * as React from 'react';
import { Button, Modal } from 'react-bootstrap';

interface Props {
  isCancelling: boolean;
  show: boolean;
  submit: () => Promise<void>;
  hide: () => void;
}

/**
 * Component for the cancel dynamic mix modal.
 */
class CancelTaskModal extends React.Component<Props, {}> {
  constructor(props: Props) {
    super(props);
  }

  submit = async (): Promise<void> => {
    await this.props.submit();
    this.props.hide();
  };

  render(): JSX.Element | null {
    const { isCancelling } = this.props;
    return (
      <Modal show={this.props.show} onHide={!isCancelling ? this.props.hide : undefined}>
        <Modal.Header closeButton>
          <Modal.Title>Cancelar Tarefa</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div>Tem certeza de que deseja cancelar esta tarefa?</div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="danger" disabled={isCancelling} onClick={this.submit}>
            Cancelar
          </Button>
        </Modal.Footer>
      </Modal>
    );
  }
}

export default CancelTaskModal;
