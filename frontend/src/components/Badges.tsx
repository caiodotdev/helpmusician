import * as React from 'react';
import { Badge } from 'react-bootstrap';

interface BadgeProps {
  className?: string;
  faded?: boolean;
  title?: string;
}

export const OriginalBadge = (props: BadgeProps): JSX.Element => {
  const { title } = props;
  return (
    <Badge className="ml-2 mr-2" pill variant="primary" title={title}>
      Original
    </Badge>
  );
};

export const AllBadge = (): JSX.Element => {
  return (
    <Badge pill variant="primary">
      Todos (Mix Dinâmica)
    </Badge>
  );
};

export const VocalsBadge = (props: BadgeProps): JSX.Element => {
  const { faded, title } = props;
  return (
    <Badge pill className={props.className} variant={faded ? 'vocals-faded' : 'vocals'} title={title}>
      Vocais
    </Badge>
  );
};

export const PianoBadge = (props: BadgeProps): JSX.Element => {
  const { faded, title } = props;
  return (
    <Badge pill className={props.className} variant={faded ? 'piano-faded' : 'piano'} title={title}>
      Piano
    </Badge>
  );
};

export const AccompBadge = (props: BadgeProps): JSX.Element => {
  const { faded, title } = props;
  return (
    <Badge pill className={props.className} variant={faded ? 'accomp-faded' : 'accomp'} title={title}>
      Outros (Acomp)
    </Badge>
  );
};

export const AccompShortBadge = (props: BadgeProps): JSX.Element => {
  const { faded, title } = props;
  return (
    <Badge pill className={props.className} variant={faded ? 'accomp-faded' : 'accomp'} title={title}>
      Outros (Acomp)
    </Badge>
  );
};

export const DrumsBadge = (props: BadgeProps): JSX.Element => {
  const { faded, title } = props;
  return (
    <Badge pill className={props.className} variant={faded ? 'drums-faded' : 'drums'} title={title}>
      Bateria
    </Badge>
  );
};

export const BassBadge = (props: BadgeProps): JSX.Element => {
  const { faded, title } = props;
  return (
    <Badge pill className={props.className} variant={faded ? 'bass-faded' : 'bass'} title={title}>
      Baixo
    </Badge>
  );
};

export const MetronomeBadge = (props: BadgeProps): JSX.Element => {
  const { faded, title } = props;
  return (
    <Badge pill className={props.className} variant={faded ? 'metronome-faded' : 'metronome'} title={title}>
      Metrônomo
    </Badge>
  );
};
